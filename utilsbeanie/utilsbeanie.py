from typing import Type

from beanie import Document

from utilsbeanie.actions import *
from utilsbeanie.utility import *


class Beanie(
    DeleteMixin,
    ExistMixin,
    FetchByAggregationPipelineMixin,
    FetchByGroupByAggregationPipelineMixin,
    FetchSimpleMixin,
    InsertMixin,
    UpdateByObjMixin,
    UpdateNoReturnMixin,
    UpdateWithReturnMixin,

    AggregationMixin,
    GroupByAggregationMixin,
    FetchSimpleMixin,
    InsertMixin,
    FilterForAggregationMixin,
    FilterForGroupByAggregationMixin,
    FilterMixin,
    HelperMixin,
):
    def __init__(
        self,
        document: Type[Document],
        field_separator: str = "__"
    ) -> None:
        self.document: Type[Document] = document
        self.field_separator = field_separator
