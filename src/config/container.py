import uuid
from typing import Optional, Any
from uuid import UUID

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Dependency, Singleton
from dependency_injector.wiring import Provide, inject  # noqa
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncEngine,
    AsyncSession,
)
from lato import Application, TransactionContext

from config.config import AppConfig
from config.provider import ContainerProvider
from modules.accounts.application import account_module
from modules.accounts.infra.repositories import AccountRepository


def create_db_engine(config: AppConfig) -> AsyncEngine:
    from seedwork.infra.database import base_registry
    engine = create_async_engine(config.db_dsn, echo=config.db_echo)
    base_registry.metadata.bind = engine
    return engine


def create_application(config, db_engine) -> Application:
    """Creates new instance of the application"""
    application = Application(
        config.title,
        app_version=0.1,
        db_engine=db_engine,
    )
    application.include_submodule(account_module)

    @application.on_create_transaction_context
    def on_create_transaction_context(**_) -> TransactionContext:
        engine = application.get_dependency("db_engine")
        session = AsyncSession(engine)
        correlation_id = uuid.uuid4()

        # create IoC container for the transaction
        dependency_provider = ContainerProvider(
            TransactionContainer(
                db_session=session,
                correlation_id=correlation_id,
            )
        )
        return TransactionContext(dependency_provider)

    @application.on_enter_transaction_context
    def on_enter_transaction_context(ctx: TransactionContext) -> None:
        ctx.set_dependencies(publish=ctx.publish)

    @application.on_exit_transaction_context
    async def on_exit_transaction_context(
        ctx: TransactionContext,
        exception: Optional[Exception] = None,
    ) -> None:
        session = ctx["db_session"]
        if exception:
            await session.rollback()
        else:
            await session.commit()
        await session.close()

    @application.transaction_middleware
    async def event_collector_middleware(ctx: TransactionContext, call_next):
        handler_kwargs = call_next.keywords

        result = call_next()
        domain_events = []
        repositories = filter(
            lambda x: hasattr(x, 'collect_events'), handler_kwargs.values()
        )
        for repo in repositories:
            domain_events.extend(repo.collect_events())
        for event in domain_events:
            ctx.publish(event)

        return result

    return application


class ApplicationContainer(DeclarativeContainer):
    config: Any = Singleton(AppConfig)
    db_engine = Singleton(create_db_engine, config)
    application = Singleton(create_application, config, db_engine)


class TransactionContainer(DeclarativeContainer):
    correlation_id = Dependency(instance_of=UUID)
    db_session = Dependency(instance_of=AsyncSession)
    account_repository: Any = Singleton(AccountRepository, session=db_session)
