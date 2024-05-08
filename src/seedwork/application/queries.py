from typing import Any, Optional

from lato import Query as LatoQuery

from seedwork.application.dtos import Result
from seedwork.domain.errors import Error
from seedwork.domain.events import generic_model_config


class Query(LatoQuery):
    """Abstract base class for all queries"""

    model_config = generic_model_config


class QueryResult(Result):
    payload: Any = None
    error: Optional[Error] = None
