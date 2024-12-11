from typing import (
    Dict,
    Generic,
    Protocol,
    runtime_checkable,
    TypeVar,
)
from time import time
from random import randrange

from beanie import (
    Document,
    SortDirection,
)
from pymongo.errors import DuplicateKeyError


@runtime_checkable
class InsertMixinProtocol(Protocol):
    document: Document


T = TypeVar("T", bound=InsertMixinProtocol)


class InsertMixin(Generic[T]):
    @staticmethod
    def calculate_epoch_pid(min: int = 1000, max: int = 10000) -> int:
        return int(f"{time():.0f}{randrange(min, max)}")
