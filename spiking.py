from lato.dependency_provider import BasicDependencyProvider


class FooService:
    pass


async def a_handler(service: FooService):
    pass


foo_service = FooService()
dp = BasicDependencyProvider(foo_service=foo_service)
assert dp[FooService] is foo_service
assert dp["foo_service"] is foo_service

# assert dp.resolve_func_params(a_handler) == {'service': foo_service}
