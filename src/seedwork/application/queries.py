from lato import Query as LatoQuery
from pydantic import ConfigDict


class Query(LatoQuery):
    model_config = ConfigDict(
        frozen=True,
        from_attributes=True,
        arbitrary_types_allowed=True,
    )
