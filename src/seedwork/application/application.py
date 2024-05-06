from collections.abc import Callable
from typing import Optional

from lato import (
    Application as LatoApplication,
    ApplicationModule as LatoApplicationModule,
)


class Application(LatoApplication):
    def start_mappers(self) -> None:
        for submodule in self._submodules:
            if mapper := getattr(submodule, "_mapper", None):
                mapper()


class ApplicationModule(LatoApplicationModule):
    def __init__(self, *args, **kw) -> None:
        super().__init__(*args, **kw)
        self._mapper: Optional[Callable] = None

    def register_mapper(self, mapper: Callable) -> None:
        self._mapper = mapper
