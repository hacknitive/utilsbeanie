from typing import (
    Generic,
    Dict,
    Protocol,
    runtime_checkable,
    TypeVar,
)

from beanie import (
    PydanticObjectId,
    Document,
)


@runtime_checkable
class DeleteMixinProtocol(Protocol):
    document: Document


T = TypeVar("T", bound=DeleteMixinProtocol)


class DeleteMixin(Generic[T]):
    async def delete_list_by_filter(
        self: T,
        filter_: Dict,
    ) -> None:
        return await self.document.find(filter_).delete()

    async def delete_one_by_filter(
        self: T,
        filter_: Dict,
    ) -> None:
        return await self.document.find_one(filter_).delete()

    async def delete_one_by_id(
        self: T,
        id_: PydanticObjectId,
    ) -> None:
        return await self.document.find_one({"_id": id_}).delete()

    async def delete_one_by_pid(
        self: T,
        pid: str,
    ) -> None:
        return await self.document.find_one({"pid": pid}).delete()
