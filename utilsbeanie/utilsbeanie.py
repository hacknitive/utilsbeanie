from typing import Type

from beanie import Document

from utilsbeanie import actions
from utilsbeanie import utility


class UtilsBeanie(
    actions.DeleteMixin,
    actions.ExistMixin,
    actions.FetchByAggregationPipelineMixin,
    actions.FetchByGroupByAggregationPipelineMixin,
    actions.FetchSimpleMixin,
    actions.InsertMixin,
    actions.UpdateByObjMixin,
    actions.UpdateNoReturnMixin,
    actions.UpdateWithReturnMixin,

    utility.AggregationMixin,
    utility.GroupByAggregationMixin,
    utility.FetchSimpleMixin,
    utility.InsertMixin,
    utility.FilterForAggregationMixin,
    utility.FilterForGroupByAggregationMixin,
    utility.FilterMixin,
    utility.HelperMixin,
):
    def __init__(
        self,
        document: Type[Document],
        field_separator: str = "__"
    ) -> None:
        self.document: Type[Document] = document
        self.field_separator = field_separator
