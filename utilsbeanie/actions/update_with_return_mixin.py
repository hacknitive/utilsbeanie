from typing import (
    Any,
    List,
    Dict,
    Type,
    Optional,
    Union,
    Tuple,
    Generic,
    Protocol,
    runtime_checkable,
    TypeVar,
)

from beanie import (
    Document,
    SortDirection,
)
from beanie.odm.documents import AsyncIOMotorClientSession
from pydantic import BaseModel

from ..constant import EnumOrderBy


@runtime_checkable
class UpdateWithReturnMixinProtocol(Protocol):
    document: Document

    @staticmethod
    def convert_order_by_to_sort(
        order_by: Dict[str, EnumOrderBy] | None = None,
    ) -> List: ...

    @staticmethod
    def prepare_skip_limit(
        current_page: Optional[int] = None,
        page_size: Optional[int] = None,
        skip: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> dict: ...



T = TypeVar("T", bound=UpdateWithReturnMixinProtocol)

class UpdateWithReturnMixin(Generic[T]):

    async def update_one_by_filter_with_return(
        self: T,
        filter_: Dict,
        inputs: dict,
        projection_model: Optional[Type[BaseModel]] = None,
        fetch_links: bool = False,
        skip: Optional[int] = None,
        limit: Optional[int] = None,
        sort: Union[None, str, List[Tuple[str, SortDirection]]] = None,
        order_by: Dict[str, EnumOrderBy] | None = None,
        session: Optional[AsyncIOMotorClientSession] = None,
        ignore_cache: bool = False,
        with_children: bool = False,
        lazy_parse: bool = False,
        nesting_depth: Optional[int] = None,
        nesting_depths_per_field: Optional[Dict[str, int]] = None,
        **pymongo_kwargs,
    ) -> Document:
        obj = await self.document.find_many(
            filter_,
            projection_model=projection_model,
            fetch_links=fetch_links,
            session=session,
            ignore_cache=ignore_cache,
            with_children=with_children,
            lazy_parse=lazy_parse,
            nesting_depth=nesting_depth,
            nesting_depths_per_field=nesting_depths_per_field,
            skip=skip,
            limit=limit,
            sort=sort,
            order_by=order_by,
            **pymongo_kwargs,
        ).first_or_none()

        for attr, value in inputs.items():
            setattr(obj, attr, value)

        await obj.save()

        return obj

    async def update_one_by_id(
        self: T,
        document_id: Any,
        inputs: dict,
        session: Optional[AsyncIOMotorClientSession] = None,
        ignore_cache: bool = False,
        fetch_links: bool = False,
        with_children: bool = False,
        nesting_depth: Optional[int] = None,
        nesting_depths_per_field: Optional[Dict[str, int]] = None,
        **pymongo_kwargs,
    ) -> Document:
        obj = await self.document.get(
            document_id=document_id,
            session=session,
            ignore_cache=ignore_cache,
            fetch_links=fetch_links,
            with_children=with_children,
            nesting_depth=nesting_depth,
            nesting_depths_per_field=nesting_depths_per_field,
            **pymongo_kwargs,
        )

        for attr, value in inputs.items():
            setattr(obj, attr, value)

        await obj.save()
        return obj

    async def update_one_by_pid(
        self: T,
        pid: int | str,
        inputs: dict,
        projection_model: Optional[Type[BaseModel]] = None,
        fetch_links: bool = False,
        session: Optional[AsyncIOMotorClientSession] = None,
        ignore_cache: bool = False,
        with_children: bool = False,
        lazy_parse: bool = False,
        nesting_depth: Optional[int] = None,
        nesting_depths_per_field: Optional[Dict[str, int]] = None,
        **pymongo_kwargs,
    ) -> Document:
        obj = await self.document.find_many(
            {"pid": pid},
            projection_model=projection_model,
            fetch_links=fetch_links,
            session=session,
            ignore_cache=ignore_cache,
            with_children=with_children,
            lazy_parse=lazy_parse,
            nesting_depth=nesting_depth,
            nesting_depths_per_field=nesting_depths_per_field,
            **pymongo_kwargs,
        ).first_or_none()

        for attr, value in inputs.items():
            setattr(obj, attr, value)

        await obj.save()
        return obj

    async def update_list_by_filter(
        self: T,
        filter_: Dict,
        inputs: dict,
        current_page: int = None,
        page_size: int = None,
        order_by: Dict[str, EnumOrderBy] | None = None,
        projection_model: Optional[Type[BaseModel]] = None,
        fetch_links: bool = False,
        skip: Optional[int] = None,
        limit: Optional[int] = None,
        sort: Union[None, List[Tuple[str, SortDirection]]] = None,
        session: Optional[AsyncIOMotorClientSession] = None,
        ignore_cache: bool = False,
        with_children: bool = False,
        lazy_parse: bool = False,
        nesting_depth: Optional[int] = None,
        nesting_depths_per_field: Optional[Dict[str, int]] = None,
        **pymongo_kwargs,
    ) -> list[Document]:
        objs = self.document.find(
            filter_,
            projection_model=projection_model,
            **self.prepare_skip_limit(
                current_page=current_page,
                page_size=page_size,
                skip=skip,
                limit=limit,
            ),
            sort=self.convert_order_by_to_sort(order_by=order_by) or sort,
            fetch_links=fetch_links,
            session=session,
            ignore_cache=ignore_cache,
            with_children=with_children,
            lazy_parse=lazy_parse,
            nesting_depth=nesting_depth,
            nesting_depths_per_field=nesting_depths_per_field,
            **pymongo_kwargs,
        )

        for obj in objs:
            for attr, value in inputs.items():
                setattr(obj, attr, value)

            await obj.save()

        return objs
