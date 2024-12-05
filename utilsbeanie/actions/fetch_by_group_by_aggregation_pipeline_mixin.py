from typing import (
    Any,
    List,
    Dict,
    Type,
    Optional,
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
from pydantic import BaseModel

from ..constant import (
    EnumOrderBy,
    DATETIME_BY_X_FORMAT,
)


@runtime_checkable
class PrepareGroupByThenFetchMixinProtocol(Protocol):
    document: Document
    field_separator: str = "__"

    async def fetch_by_aggregation_pipeline(
        self,
        aggregation_pipeline: Optional[List[Dict]] = None,
        first_filter: dict = None,
        last_filter: dict = None,
        sort: dict[str, SortDirection] = None,
        order_by: Dict[str, EnumOrderBy] | None = None,
        projection_model: Optional[Type[BaseModel]] = None,
        skip: Optional[int] = None,
        limit: Optional[int] = None,
        current_page: int = None,
        page_size: int = None,
    ) -> List[Type[BaseModel] | Dict]: ...

    def prepare_filter_for_group_by_aggregation(
        self,
        inputs: Dict[str, Any],
        fields_names_for_regex: Tuple[str, ...] = tuple(),
        fields_names_for_range: Tuple[str, ...] = tuple(),
        fields_names_for_in: Tuple[str, ...] = tuple(),
        search_field_name: str = None,
        fields_names_for_search: Tuple[str, ...] = tuple(),
    ) -> tuple[dict, dict, dict]: ...

    def create_group_by_pipeline(self, group_by_on: list[str]) -> List[Dict]: ...

    async def fetch_by_aggregation_pipeline_with_pagination(
        self,
        aggregation_pipeline: Optional[List[Dict]] = None,
        first_filter: dict = None,
        last_filter: dict = None,
        sort: dict[str, SortDirection] = None,
        order_by: Dict[str, EnumOrderBy] | None = None,
        current_page: int = 1,
        page_size: int = 10,
        projection_model: Optional[Type[BaseModel]] = None,
        skip: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> Dict: ...



T = TypeVar("T", bound=PrepareGroupByThenFetchMixinProtocol)


class FetchByGroupByAggregationPipelineMixin(Generic[T]):
    async def fetch_by_group_by_aggregation_pipeline(
        self: T,
        aggregation_pipeline: list[dict],
        inputs: dict,
        group_by_on: list[str],
        search_field_name: str = "search",
        fields_names_for_regex: tuple[str, ...] = tuple(),
        fields_names_for_range: tuple[str, ...] = tuple(),
        fields_names_for_in: tuple[str, ...] = tuple(),
        fields_names_for_search: tuple[str, ...] = tuple(),
        order_by: dict[str, EnumOrderBy] | None = None,
        sort: dict[str, SortDirection] = None,
        projection_model: Optional[Type[BaseModel]] = None,
        skip: Optional[int] = None,
        limit: Optional[int] = None,
        current_page: int = None,
        page_size: int = None,
    ) -> dict:
        first_filter, middle_filter, last_filter = (
            self.prepare_filter_for_group_by_aggregation(
                inputs=inputs,
                search_field_name=search_field_name,
                fields_names_for_regex=fields_names_for_regex,
                fields_names_for_range=fields_names_for_range,
                fields_names_for_in=fields_names_for_in,
                fields_names_for_search=fields_names_for_search,
            )
        )

        return await self.fetch_by_aggregation_pipeline(
            aggregation_pipeline=[
                *aggregation_pipeline,
                {"$match": middle_filter},
                *self.create_group_by_pipeline(group_by_on=group_by_on),
            ],
            first_filter=first_filter,
            last_filter=last_filter,
            order_by=order_by,
            sort=sort,
            projection_model=projection_model,
            skip=skip,
            limit=limit,
            current_page=current_page,
            page_size=page_size,
        )

    async def fetch_by_group_by_aggregation_pipeline_with_pagination(
        self: T,
        aggregation: list[dict],
        inputs: dict,
        group_by_on: list[str],
        current_page: int = 1,
        page_size: int = 10,
        search_field_name: str = "search",
        fields_names_for_regex: tuple[str, ...] = tuple(),
        fields_names_for_range: tuple[str, ...] = tuple(),
        fields_names_for_in: tuple[str, ...] = tuple(),
        fields_names_for_search: tuple[str, ...] = tuple(),
        order_by: dict[str, EnumOrderBy] | None = None,
        sort: dict[str, SortDirection] = None,
        projection_model: Optional[Type[BaseModel]] = None,
        skip: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> dict:
        first_filter, middle_filter, last_filter = (
            self.prepare_filter_for_group_by_aggregation(
                inputs=inputs,
                search_field_name=search_field_name,
                fields_names_for_regex=fields_names_for_regex,
                fields_names_for_range=fields_names_for_range,
                fields_names_for_in=fields_names_for_in,
                fields_names_for_search=fields_names_for_search,
            )
        )

        if middle_filter:
            aggregation = [
                *aggregation,
                {"$match": middle_filter},
                *self.create_group_by_pipeline(group_by_on=group_by_on),
            ]
        else:
            aggregation = [
                *aggregation,
                *self.create_group_by_pipeline(group_by_on=group_by_on),
            ]

        return await self.fetch_by_aggregation_pipeline_with_pagination(
            aggregation_pipeline=aggregation,
            first_filter=first_filter,
            last_filter=last_filter,
            order_by=order_by,
            current_page=current_page,
            page_size=page_size,
            skip=skip,
            limit=limit,
            sort=sort,
            projection_model=projection_model,
        )

