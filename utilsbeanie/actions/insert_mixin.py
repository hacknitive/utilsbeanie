from typing import (
    Dict,
    Generic,
    Protocol,
    runtime_checkable,
    TypeVar,
)

from beanie import Document
from pymongo.errors import DuplicateKeyError


@runtime_checkable
class InsertMixinProtocol(Protocol):
    document: Document

    @staticmethod
    def calculate_epoch_pid(min: int = 1000, max: int = 10000) -> int: ...


T = TypeVar("T", bound=InsertMixinProtocol)


class InsertMixin(Generic[T]):
    async def insert_one_without_pid(
        self: T,
        inputs: Dict,
    ) -> Document:
        obj = self.document(**inputs)
        await obj.insert()
        return obj

    async def insert_one_by_epoch_pid(self: T, inputs: Dict, min=1000, max=10000) -> Document:
        while True:
            try:
                inputs_with_pid = {
                    "pid": self.calculate_epoch_pid(min=min, max=max),
                    **inputs,
                }
                obj = self.document(**inputs_with_pid)
                await obj.insert()
                return obj
            except DuplicateKeyError as e:
                if not getattr(e, "details", None):
                    raise
                if e.details.get("keyPattern") != {"pid": 1}:
                    raise
