from typing import (
    Generic,
    Callable,
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
class ExistMixinProtocol(Protocol):
    document: Document


T = TypeVar("T", bound=ExistMixinProtocol)


class ExistMixin(Generic[T]):
    async def is_one_item_absent_by_filter(
        self: T,
        filter_: dict,
        raise_on_existence: bool = False,
        exception_creater_func: Callable = None,
    ) -> bool:
        result = await self.document.find_one(
            filter_,
        ).exists()

        if result:
            if raise_on_existence:
                raise exception_creater_func(
                    document=self.document,
                    filter_=filter_,
                    method_name="is_one_item_absent_by_filter",
                )

            return False

        else:
            return True

    async def is_one_item_absent_by_id(
        self: T,
        id_: PydanticObjectId,
        raise_on_existence: bool = False,
        exception_creater_func: callable = None,
    ) -> bool:
        result = await self.document.find_one(
            {"_id": id_},
            fetch_links=False,
        ).exists()

        if result:
            if raise_on_existence:
                raise exception_creater_func(
                    id_=id_,
                    document=self.document,
                    method_name="is_one_item_absent_by_id",
                )

            return False

        else:
            return True

    async def is_one_item_absent_by_pid(
        self: T,
        pid: int | str,
        raise_on_existence: bool = False,
        exception_creater_func: callable = None,
    ) -> bool:
        result = await self.document.find_one(
            {"pid": pid},
            fetch_links=False,
        ).exists()

        if result:
            if raise_on_existence:
                raise exception_creater_func(
                    pid=pid,
                    document=self.document,
                    method_name="is_one_item_absent_by_pid",
                )

            return False

        else:
            return True

    async def is_one_item_exist_by_filter(
        self: T,
        filter_: dict,
        fetch_links: bool = False,
        raise_on_absence: bool = False,
        exception_creater_func: callable = None,
    ) -> bool:
        result = await self.document.find_one(
            filter_,
            fetch_links=fetch_links,
        ).exists()

        if result:
            return True

        else:
            if raise_on_absence:
                raise exception_creater_func(
                    filter_=filter_,
                    document=self.document,
                    method_name="is_one_item_exist_by_filter",
                )

            return False

    async def is_one_item_exist_by_id(
        self: T,
        id_: PydanticObjectId,
        raise_on_absence: bool = False,
        exception_creater_func: callable = None,
    ) -> bool:
        result = await self.document.find_one(
            {"_id": id_},
            fetch_links=False,
        ).exists()

        if result:
            return True

        else:
            if raise_on_absence:
                raise exception_creater_func(
                    id_=id_,
                    document=self.document,
                    method_name="is_one_item_exist_by_id",
                )

            return False

    async def is_one_item_exist_by_pid(
        self: T,
        pid: int | str,
        raise_on_absence: bool = False,
        exception_creater_func: callable = None,
    ) -> bool:
        result = await self.document.find_one(
            {"pid": pid},
            fetch_links=False,
        ).exists()

        if result:
            return True

        else:
            if raise_on_absence:
                raise exception_creater_func(
                    pid=pid,
                    document=self.document,
                    method_name="is_one_item_exist_by_pid",
                )

            return False
