from lato import TransactionContext


async def event_collector_middleware(ctx: TransactionContext, call_next):
    handler_kwargs = call_next.keywords

    result = await call_next()
    domain_events = []
    repositories = filter(
        lambda x: hasattr(x, 'collect_events'), handler_kwargs.values()
    )
    for repo in repositories:
        domain_events.extend(repo.collect_events())
    for event in domain_events:
        ctx.publish(event)

    return result


async def error_handling_middleware(ctx: TransactionContext, call_next):
    res = await call_next()
    print(f"{res=}")
    return res
