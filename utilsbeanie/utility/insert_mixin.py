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
    def calculate_epoch_pid() -> int:
        return int(f"{time():.0f}{randrange(1000, 10000)}")

    async def calculate_incremental_pid(
        self: T,
    ) -> int:
        result = await self.document.find_many(
            {}, sort=[("pid", SortDirection.DESCENDING)]
        ).first_or_none()
        return 1 if result is None else result.pid + 1
