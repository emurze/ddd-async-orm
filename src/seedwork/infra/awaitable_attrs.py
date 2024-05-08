from typing import Any, Awaitable

from sqlalchemy.exc import MissingGreenlet
from sqlalchemy.util import greenlet_spawn

from seedwork.domain.entities import AggregateRoot, AwaitableAttrs


class GenericAwaitableAttrs:
    __slots__ = "_instance"

    def __init__(self, _instance: Any) -> None:
        self._instance = _instance

    @classmethod
    def wrap(cls, entity: AggregateRoot) -> AwaitableAttrs:
        return AwaitableAttrs(awaitable_attrs=cls(entity))


class SqlAlchemyAwaitableAttrs(GenericAwaitableAttrs):
    """Loads lazy sqlalchemy attributes and relations asynchronously."""

    def __getattr__(self, name: str) -> Awaitable[Any]:
        return greenlet_spawn(getattr, self._instance, name)


class MemoryAwaitableAttrs(GenericAwaitableAttrs):
    """Loads lazy memory attributes and relations asynchronously."""

    def __init__(self, *args, **kw) -> None:
        super().__init__(*args, **kw)
        self._loaded_objs: list = []

    def _set_loading_marker(self, obj: Any) -> Any:
        """Marks obj as loaded and appends it to the list of loaded objects."""
        obj._is_loaded = True
        self._loaded_objs.append(obj)
        return obj

    def __getattr__(self, name: str) -> Awaitable[Any]:
        async def wrapper():
            return self._set_loading_marker(
                getattr(self._instance, f"__loading{name}")
            )

        getter = object.__getattribute__
        return getter(self, name) if name.startswith("_") else wrapper()

    def getattr(self, name: str) -> Any:
        """Gets attributes and raises errors if relations are not loaded."""

        if name.startswith("__loading"):
            return object.__getattribute__(self, name.replace("__loading", ""))

        obj = object.__getattribute__(self, name)
        if hasattr(obj, "_sa_adapter") and not getattr(obj, "_is_loaded", ""):
            raise MissingGreenlet()
        else:
            return obj
