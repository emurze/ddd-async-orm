import enum
from dataclasses import dataclass
from typing import Self


class ErrorType(str, enum.Enum):
    CONFLICT: str = "Resource conflict error"
    VALIDATION: str = "Validation error"
    PARAMETERS: str = "Parameters error"
    NOT_FOUND: str = "Resource not found"
    UNAUTHORIZED: str = "Unauthorized error"
    FORBIDDEN: str = "Resource forbidden"
    SYSTEM: str = "Internal system error"


@dataclass(frozen=True, slots=True)
class Error:
    type: str
    detail: list | str

    @classmethod
    def conflict(cls, detail: str = ErrorType.CONFLICT) -> Self:
        return cls(type=ErrorType.CONFLICT, detail=detail)

    @classmethod
    def validation(cls, detail: list) -> Self:
        return cls(type=ErrorType.VALIDATION, detail=detail)

    @classmethod
    def not_found(cls, detail: str = ErrorType.NOT_FOUND) -> Self:
        return cls(type=ErrorType.NOT_FOUND, detail=detail)

    @classmethod
    def unauthorized(cls, detail: str = ErrorType.UNAUTHORIZED) -> Self:
        return cls(type=ErrorType.UNAUTHORIZED, detail=detail)

    @classmethod
    def forbidden(cls, detail: str = ErrorType.FORBIDDEN) -> Self:
        return cls(type=ErrorType.FORBIDDEN, detail=detail)

    @classmethod
    def system(cls, detail: str = ErrorType.SYSTEM) -> Self:
        return cls(type=ErrorType.SYSTEM, detail=detail)


class EntityAlreadyExistsError(Exception):
    pass


class BusinessRuleValidationException(Exception):
    def __init__(self, rule):
        self.rule = rule

    def __str__(self):
        return str(self.rule)
