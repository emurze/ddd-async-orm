import uuid
from typing import Any, Optional
from uuid import UUID

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Dependency, Singleton
from dependency_injector.wiring import Provide, inject  # noqa
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncEngine,
    AsyncSession,
)
from lato import TransactionContext

from config.api_config import ApiConfig
from config.middlewares import (
    event_collector_middleware,
    error_handling_middleware,
)
from config.provider import ContainerProvider
from modules.accounts.application import accounts_module
from modules.accounts.infra.repositories import AccountSqlAlchemyRepository
from modules.notifications.application import notifications_module
from seedwork.application.application import Application
from seedwork.infra.inbox_outbox import start_outbox_mappers, \
    SqlAlchemyMessageOutbox


def create_db_engine(config: ApiConfig) -> AsyncEngine:
    from seedwork.infra.database import base_registry

    engine = create_async_engine(config.db_dsn, echo=config.db_echo)
    base_registry.metadata.bind = engine
    return engine


def create_application(config, db_engine) -> Application:
    """Creates new instance of the application."""
    application = Application(
        config.title,
        app_version=0.1,
        db_engine=db_engine,
        mappers=[start_outbox_mappers],
    )
    application.include_submodule(accounts_module)
    application.include_submodule(notifications_module)
    application.start_mappers()

    @application.on_create_transaction_context
    def on_create_transaction_context(**_) -> TransactionContext:
        engine = application.get_dependency("db_engine")
        session = AsyncSession(engine)
        correlation_id = uuid.uuid4()

        # Create IoC container for the transaction
        dependency_provider = ContainerProvider(
            TransactionContainer(
                db_session=session,
                correlation_id=correlation_id,
            )
        )
        return TransactionContext(dependency_provider)

    @application.on_enter_transaction_context
    def on_enter_transaction_context(ctx: TransactionContext) -> None:
        message_outbox = SqlAlchemyMessageOutbox(ctx["db_session"])
        ctx.set_dependencies(
            publish=message_outbox.publish,
            is_error=False,
        )

    application.transaction_middleware(event_collector_middleware)
    application.transaction_middleware(error_handling_middleware)

    @application.on_exit_transaction_context
    async def on_exit_transaction_context(
        ctx: TransactionContext,
        exception: Optional[Exception] = None,
    ):
        session = ctx["db_session"]
        if exception or ctx["is_error"]:
            await session.rollback()
        else:
            await session.commit()
        await session.close()

    return application


class ApplicationContainer(DeclarativeContainer):
    config: Any = Singleton(ApiConfig)
    db_engine = Singleton(create_db_engine, config)
    application = Singleton(create_application, config, db_engine)


class TransactionContainer(DeclarativeContainer):
    correlation_id = Dependency(instance_of=UUID)
    db_session = Dependency(instance_of=AsyncSession)
    account_repository: Any = Singleton(
        AccountSqlAlchemyRepository, session=db_session
    )


app_container = ApplicationContainer()
