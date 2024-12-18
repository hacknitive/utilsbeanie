from typing import (
    List,
    Dict,
    Protocol,
    runtime_checkable,
    TypeVar,
    Generic,
)

from ..constant import DATETIME_BY_X_FORMAT


@runtime_checkable
class GroupByAggregationMixinProtocol(Protocol):
    field_separator: str = "__"


T = TypeVar("T", bound=GroupByAggregationMixinProtocol)


class GroupByAggregationMixin(Generic[T]):
    def build_group_by_pipeline(
        self: T,
        group_by_on: list[str],
    ) -> List[Dict]:
        aggregation_pipeline = []
        add_field, group_id = self._prepare_fields(group_by_on)

        if add_field:
            aggregation_pipeline.append({"$addFields": add_field})

        aggregation_pipeline.append(
            {"$group": {"_id": group_id, "count": {"$sum": 1}}},
        )

        return aggregation_pipeline

    def _prepare_fields(self, group_by_on: list[str]) -> tuple[Dict, Dict]:
        add_field = {}
        group_id = {}
        for field_alias_name in group_by_on:
            field_real_name = field_alias_name.replace(self.field_separator, ".")

            if field_real_name.endswith(tuple(DATETIME_BY_X_FORMAT.keys())):
                field_alias_name, field_real_name = self._process_datetime_field(field_alias_name, field_real_name)
                if field_alias_name and field_real_name:
                    add_field[field_alias_name] = {
                        "$dateToString": {
                            "format": DATETIME_BY_X_FORMAT[field_real_name],
                            "date": f"${field_real_name}",
                        }
                    }

            group_id[field_alias_name] = f"${field_real_name}"

        return add_field, group_id

    def _process_datetime_field(self, alias_name: str, real_name: str) -> tuple[str, str]:
        for datetime_key, datetime_value in DATETIME_BY_X_FORMAT.items():
            if real_name.endswith(datetime_key):
                alias_name = alias_name.replace(datetime_key, "")
                real_name = real_name.replace(datetime_key, "")
                return alias_name, real_name
        return alias_name, real_name

    @staticmethod
    def build_group_by_attributes(attributes_names: tuple[str, ...]) -> list[str]:
        group_by_attributes = list()
        for i in attributes_names:
            if i.endswith("_at"):
                for j in DATETIME_BY_X_FORMAT.keys():
                    group_by_attributes.append(f"{i}{j}")

            else:
                group_by_attributes.append(i)

        return group_by_attributes
