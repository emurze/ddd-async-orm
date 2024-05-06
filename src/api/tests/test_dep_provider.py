import pytest
from lato.dependency_provider import BasicDependencyProvider


class DependencyProvider(BasicDependencyProvider):
    allow_names = True
    allow_types = True


class FooService:
    pass


class BarService:
    pass


async def a_handler(service: FooService | None = None):
    assert service is not None


@pytest.mark.unit
def test_can_getitem() -> None:
    service = FooService()
    provider = DependencyProvider(best_foo_service=service)
    assert provider[FooService] is service
    assert provider["best_foo_service"] is service


@pytest.mark.unit
def test_can_get_dependency() -> None:
    service = FooService()
    provider = DependencyProvider(best_foo_service=service)
    assert provider.get_dependency(FooService) is service
    assert provider.get_dependency("best_foo_service") is service


@pytest.mark.unit
def test_can_register_dependency() -> None:
    service = FooService()
    provider = DependencyProvider()
    provider.register_dependency("best_foo_service", service)
    provider.register_dependency(FooService, service)
    assert provider[FooService] is service
    assert provider["best_foo_service"] is service


@pytest.mark.unit
def test_can_has_dependency() -> None:
    provider = DependencyProvider(best_foo_service=FooService())
    assert provider.has_dependency("best_foo_service")


@pytest.mark.unit
def test_can_copy() -> None:
    provider = DependencyProvider(best_foo_service=FooService())
    new_provider = provider.copy()
    assert len(provider._dependencies) == 2
    assert getattr(new_provider, "_dependencies") == provider._dependencies
    assert new_provider is not provider


@pytest.mark.unit
def test_can_setitem() -> None:
    service = FooService()
    provider = DependencyProvider()
    provider[FooService] = service
    assert provider[FooService] is service


@pytest.mark.unit
async def test_resolve_func_params() -> None:
    provider = DependencyProvider(  # Tolerant reader
        best_foo_service=FooService(),
        bar_service=FooService(),
    )
    params = provider.resolve_func_params(a_handler)
    await a_handler(**params)
