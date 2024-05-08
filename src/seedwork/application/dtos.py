from pydantic import BaseModel

from seedwork.domain.errors import Error
from seedwork.domain.events import generic_model_config


class DTO(BaseModel):
    model_config = generic_model_config


class SuccessMixin:
    error: Error

    def is_success(self) -> bool:
        return not self.error

    def is_failure(self) -> bool:
        return not self.is_success()


class Result(DTO, SuccessMixin):
    pass
