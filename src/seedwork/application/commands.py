from lato import Command as LatoCommand
from pydantic import ConfigDict


class Command(LatoCommand):
    """Abstract base class for all commands"""
    model_config = ConfigDict(
        frozen=True,
        from_attributes=True,
        arbitrary_types_allowed=True,
    )
