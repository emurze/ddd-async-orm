from collections.abc import Callable

from lato import TransactionContext
from lato.message import Message

from seedwork.application.commands import CommandResult, Command
from seedwork.application.dtos import Result
from seedwork.application.events import EventResult
from seedwork.application.queries import QueryResult, Query
from seedwork.domain.errors import Error


async def event_collector_middleware(ctx: TransactionContext, call_next):
    handler_kwargs = call_next.keywords

    result = await call_next()
    domain_events = []
    repositories = filter(
        lambda x: hasattr(x, "collect_events"), handler_kwargs.values()
    )
    for repo in repositories:
        domain_events.extend(repo.collect_events())
    for event in domain_events:
        ctx.publish(event)

    return result


async def error_handling_middleware(
    ctx: TransactionContext,
    call_next: Callable,
) -> Result:
    """Middleware for error handling."""
    result = await call_next()
    if isinstance(result, Result):
        return result
    elif isinstance(result, Error):
        ctx.set_dependencies(is_error=True)
        result_class = _get_result_class(ctx['message'])
        return result_class(error=result)
    else:
        result_class = _get_result_class(ctx['message'])
        return result_class(payload=result)


def _get_result_class(message: Message) -> type[Result]:
    if isinstance(message, Command):
        return CommandResult
    elif isinstance(message, Query):
        return QueryResult
    else:
        return EventResult
