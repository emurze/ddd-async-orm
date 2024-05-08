from typing import Any, Optional

from lato import Command as LatoCommand

from seedwork.application.dtos import Result
from seedwork.domain.errors import Error
from seedwork.domain.events import DomainEvent, generic_model_config


class Command(LatoCommand):
    """Abstract base class for all commands"""

    model_config = generic_model_config


class CommandResult(Result):
    payload: Any = None
    events: list[DomainEvent] = []
    error: Optional[Error] = None
