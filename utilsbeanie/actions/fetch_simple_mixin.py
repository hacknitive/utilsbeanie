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
class FetchSimpleMixinProtocol(Protocol):
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

    def create_fetch_list_by_filter_query(
        self,
        filter_: Dict,
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
    ): ...


T = TypeVar("T", bound=FetchSimpleMixinProtocol)


class FetchSimpleMixin(Generic[T]):

    async def fetch_one_by_id(
        self: T,
        document_id: Any,
        session: Optional[AsyncIOMotorClientSession] = None,
        ignore_cache: bool = False,
        fetch_links: bool = False,
        with_children: bool = False,
        nesting_depth: Optional[int] = None,
        nesting_depths_per_field: Optional[Dict[str, int]] = None,
        **pymongo_kwargs,
    ) -> Document:
        return await self.document.get(
            document_id=document_id,
            session=session,
            ignore_cache=ignore_cache,
            fetch_links=fetch_links,
            with_children=with_children,
            nesting_depth=nesting_depth,
            nesting_depths_per_field=nesting_depths_per_field,
            **pymongo_kwargs,
        )

    async def fetch_one_by_pid(
        self: T,
        pid: int | str,
        projection_model: Optional[Type[BaseModel]] = None,
        fetch_links: bool = False,
        session: Optional[AsyncIOMotorClientSession] = None,
        ignore_cache: bool = False,
        with_children: bool = False,
        lazy_parse: bool = False,
        nesting_depth: Optional[int] = None,
        nesting_depths_per_field: Optional[Dict[str, int]] = None,
        **pymongo_kwargs,
    ) -> Document | None:
        return await self.document.find_many(
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

    async def fetch_one_by_filter(
        self: T,
        filter_: Dict,
        projection_model: Optional[Type[BaseModel]] = None,
        fetch_links: bool = False,
        skip: Optional[int] = None,
        sort: Union[None, str, List[Tuple[str, SortDirection]]] = None,
        order_by: Dict[str, EnumOrderBy] | None = None,
        session: Optional[AsyncIOMotorClientSession] = None,
        ignore_cache: bool = False,
        with_children: bool = False,
        lazy_parse: bool = False,
        nesting_depth: Optional[int] = None,
        nesting_depths_per_field: Optional[Dict[str, int]] = None,
        **pymongo_kwargs,
    ) -> Document | None:
        return await self.document.find_many(
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
            limit=1,
            sort=self.convert_order_by_to_sort(order_by=order_by) or sort,
            **pymongo_kwargs,
        ).first_or_none()

    async def fetch_list_by_filter(
        self: T,
        filter_: Dict,
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
    ) -> List[Document | Dict]:
        return await self.create_fetch_list_by_filter_query(
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
        ).to_list()

    async def fetch_list_by_filter_with_pagination(
        self: T,
        filter_: Dict,
        current_page: int = None,
        page_size: int = None,
        order_by: Dict[str, EnumOrderBy] | None = None,
        projection_model: Optional[Type[BaseModel]] = None,
        fetch_links: bool = False,
        sort: Union[None, List[Tuple[str, SortDirection]]] = None,
        session: Optional[AsyncIOMotorClientSession] = None,
        ignore_cache: bool = False,
        with_children: bool = False,
        lazy_parse: bool = False,
        nesting_depth: Optional[int] = None,
        nesting_depths_per_field: Optional[Dict[str, int]] = None,
        **pymongo_kwargs,
    ) -> dict:
        query = self.create_fetch_list_by_filter_query(
            filter_,
            projection_model=projection_model,
            **self.prepare_skip_limit(
                current_page=current_page,
                page_size=page_size,
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

        result = await query.to_list()
        count = await query.count()

        return {
            "pagination": {
                "total": count,
                "current": current_page,
                "page_size": page_size or count,
            },
            "data": result,
        }

    async def fetch_count(
        self: T,
        filter_: Dict,
    ) -> int:
        return await self.document.find(filter_).count()
