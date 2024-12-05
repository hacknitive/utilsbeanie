from typing import (
    List,
    Dict,
    Type,
    Optional,
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

from ..constant import EnumOrderBy

@runtime_checkable
class FetchByAggregationPipelineMixinProtocol(Protocol):
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

    @staticmethod
    def prepare_skip_limit_for_aggregation(
        current_page: Optional[int] = None,
        page_size: Optional[int] = None,
        skip: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> list[dict]: ...


T = TypeVar("T", bound=FetchByAggregationPipelineMixinProtocol)


class FetchByAggregationPipelineMixin(Generic[T]):
    async def fetch_by_aggregation_pipeline(
        self: T,
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
    ) -> List[Type[BaseModel] | Dict]:

        skip_limit_list = self.prepare_skip_limit_for_aggregation(
            current_page=current_page,
            page_size=page_size,
            skip=skip,
            limit=limit,
        )

        sort = self.convert_order_by_to_sort(order_by=order_by) or sort

        _aggregation_pipeline = list()

        if first_filter:
            _aggregation_pipeline.append({"$match": first_filter})

        if aggregation_pipeline:
            _aggregation_pipeline.extend(aggregation_pipeline)

        if last_filter:
            _aggregation_pipeline.append({"$match": last_filter})

        if sort:
            _aggregation_pipeline.append({"$sort": sort})

        if skip_limit_list:
            _aggregation_pipeline.extend(skip_limit_list)

        return (
            await self.document.find({})
            .aggregate(
                aggregation_pipeline=_aggregation_pipeline,
                projection_model=projection_model,
            )
            .to_list()
        )

    async def fetch_by_aggregation_pipeline_with_pagination(
        self: T,
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
    ) -> Dict:


        sort = self.convert_order_by_to_sort(order_by=order_by) or sort

        skip_limit_list = self.prepare_skip_limit_for_aggregation(
            current_page=current_page,
            page_size=page_size,
            skip=skip,
            limit=limit,
        )

        _aggregation_pipeline_for_result = list()
        _aggregation_pipeline_for_count = list()

        if first_filter:
            _aggregation_pipeline_for_result.append({"$match": first_filter})
            _aggregation_pipeline_for_count.append({"$match": first_filter})

        if aggregation_pipeline:
            _aggregation_pipeline_for_result.extend(aggregation_pipeline)
            _aggregation_pipeline_for_count.extend(aggregation_pipeline)

        if last_filter:
            _aggregation_pipeline_for_result.append({"$match": last_filter})
            _aggregation_pipeline_for_count.append({"$match": last_filter})

        if sort:
            _aggregation_pipeline_for_result.append({"$sort": sort})

        if skip_limit_list:
            _aggregation_pipeline_for_result.extend(skip_limit_list)

        _aggregation_pipeline_for_count.append({"$count": "count"})

        result = (
            await self.document.find({})
            .aggregate(
                aggregation_pipeline=_aggregation_pipeline_for_result,
                projection_model=projection_model,
            )
            .to_list()
        )

        count = (
            await self.document.find({})
            .aggregate(_aggregation_pipeline_for_count)
            .to_list()
        )
        count = 0 if not count else count[0]["count"]

        return {
            "pagination": {
                "total": count,
                "current": current_page,
                "page_size": limit or page_size or count,
            },
            "data": result,
        }

