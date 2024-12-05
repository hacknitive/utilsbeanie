from typing import (
    List,
    Dict,
    Optional,
    Protocol,
    runtime_checkable,
    TypeVar,
    Generic,
)

from ..constant import (
    EnumOrderBy,
    ASCENDING,
    DESCENDING,
)

from ..constant import EnumOrderBy


@runtime_checkable
class UtilityMixinProtocol(Protocol):
    field_separator: str = "__"


T = TypeVar("T", bound=UtilityMixinProtocol)


class UtilityMixin(Generic[T]):
    @staticmethod
    def prepare_skip_limit(
        current_page: Optional[int] = None,
        page_size: Optional[int] = None,
        skip: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> dict:
        skip_limit_dictionary = dict()

        if skip:
            skip_limit_dictionary["skip"] = skip

        if limit:
            skip_limit_dictionary["limit"] = limit

        if skip_limit_dictionary:
            return skip_limit_dictionary

        if page_size > 0:
            number_of_document_2_skip = max(current_page - 1, 0) * page_size

            skip_limit_dictionary["skip"] = number_of_document_2_skip
            skip_limit_dictionary["limit"] = page_size

        return skip_limit_dictionary

    @staticmethod
    def prepare_skip_limit_for_aggregation(
        current_page: Optional[int] = None,
        page_size: Optional[int] = None,
        skip: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> list[dict]:
        skip_limit_list = list()
        if skip:
            skip_limit_list.append({"$skip": skip})

        if limit:
            skip_limit_list.append({"$skip": limit})

        if skip_limit_list:
            return skip_limit_list

        if page_size > 0:
            number_of_document_to_skip = max(current_page - 1, 0) * page_size
            skip_limit_list = [
                {"$skip": number_of_document_to_skip},
                {"$limit": page_size},
            ]

        return skip_limit_list

    def convert_order_by_to_sort_for_aggregation(
        self:T,
        order_by: Dict[str, EnumOrderBy] | None = None,
    ) -> List:
        if order_by is None:
            return None

        list_of_sorting = list()
        for key, value in order_by.items():
            order = ASCENDING if value == EnumOrderBy.ASCENDING else DESCENDING
            list_of_sorting.append((key.replace(self.field_separator, "."), order))

        return list_of_sorting