from typing import (
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


T = TypeVar("T", bound=FetchSimpleMixinProtocol)


class FetchSimpleMixin(Generic[T]):

    def create_fetch_list_by_filter_query(
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
    ):
        return self.document.find(
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
