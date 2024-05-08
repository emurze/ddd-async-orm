import inspect
from typing import Optional

from dependency_injector import providers
from dependency_injector.containers import Container
from dependency_injector.providers import (
    Dependency,
    Factory,
    Provider,
    Singleton,
)
from dependency_injector.wiring import Provide, inject  # noqa
from lato import DependencyProvider
import copy


def resolve_provider_by_type(
    container: Container, cls: type
) -> Optional[Provider]:
    def inspect_provider(provider: Provider) -> bool:
        if isinstance(provider, (Factory, Singleton)):
            return issubclass(provider.cls, cls)
        elif isinstance(provider, Dependency):
            return issubclass(provider.instance_of, cls)

        return False

    matching_providers = inspect.getmembers(
        container,
        inspect_provider,
    )
    if matching_providers:
        if len(matching_providers) > 1:
            raise ValueError(
                f"Cannot uniquely resolve {cls}. "
                f"Found {len(providers)} "  # type: ignore # noqa
                f"matching providers."
            )
        return matching_providers[0][1]
    return None


class ContainerProvider(DependencyProvider):
    """Translates container dependencies for injection into services."""

    def __init__(self, container: Container):
        self.container = container
        self.counter = 0

    def has_dependency(self, identifier: str | type) -> bool:  # type: ignore
        if isinstance(identifier, type) and resolve_provider_by_type(
            self.container, identifier
        ):
            return True
        if type(identifier) is str:
            return identifier in self.container.providers

    def register_dependency(self, identifier, dependency_instance):
        pr = providers.Object(dependency_instance)
        try:
            setattr(self.container, identifier, pr)
        except TypeError:
            setattr(self.container, f"{str(identifier)}-{self.counter}", pr)
            self.counter += 1

    def get_dependency(self, identifier):
        try:
            if isinstance(identifier, type):
                provider = resolve_provider_by_type(self.container, identifier)
            else:
                provider = getattr(self.container, identifier)
            instance = provider()
        except Exception as e:
            raise e
        return instance

    def copy(self, *args, **kwargs):
        dp = ContainerProvider(copy.copy(self.container))
        dp.update(*args, **kwargs)
        return dp
