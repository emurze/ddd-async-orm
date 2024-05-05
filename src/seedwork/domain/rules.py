import abc

from pydantic import BaseModel, ConfigDict


class BusinessRule(BaseModel):
    """This is a base class for implementing domain rules"""
    model_config = ConfigDict(arbitrary_types_allowed=True)
    __message: str = "Business rule is broken"

    def get_message(self) -> str:
        return self.__message

    @abc.abstractmethod
    def is_broken(self) -> bool: ...

    def __str__(self):
        return f"{self.__class__.__name__} {super().__str__()}"
