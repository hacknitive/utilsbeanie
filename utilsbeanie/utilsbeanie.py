from typing import Type

from beanie import Document

from utilsbeanie.actions import *
from utilsbeanie.utility import *


class UtilsBeanie(
    DeleteMixin,
    ExistMixin,
    FetchByAggregationPipelineMixin,
    FetchByGroupByAggregationPipelineMixin,
    FetchSimpleMixin,
    InsertMixin,
    UpdateByObjMixin,
    UpdateNoReturnMixin,
    UpdateWithReturnMixin,

    CreateAggregationPipeLineUtilsMixin,
    CreateGroupByAggregationUtilsMixin,
    FetchSimpleUtilsMixin,
    InsertUtilsMixin,
    PrepareFilterForAggregationUtilsMixin,
    PrepareFilterForGroupByAggregationUtilsMixin,
    PrepareFilterUtilsMixin,
    UtilityMixin,
):
    def __init__(
        self,
        document: Type[Document],
        field_separator: str = "__"
    ) -> None:
        self.document: Type[Document] = document
        self.field_separator = field_separator
