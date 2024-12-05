from typing import (
    Any,
    Dict,
    Tuple,
    Protocol,
    runtime_checkable,
    TypeVar,
    Generic,
)


@runtime_checkable
class PrepareFilterForAggregationUtilsMixinProtocol(Protocol):
    field_separator: str = "__"

    def prepare_filter(
        self,
        inputs: Dict[str, Any],
        fields_names_for_regex: Tuple[str, ...] = tuple(),
        fields_names_for_range: Tuple[str, ...] = tuple(),
        fields_names_for_in: Tuple[str, ...] = tuple(),
        search_field_name: str = None,
        fields_names_for_search: Tuple[str, ...] = tuple(),
    ) -> dict: ...


T = TypeVar("T", bound=PrepareFilterForAggregationUtilsMixinProtocol)


class PrepareFilterForAggregationUtilsMixin(Generic[T]):
    def prepare_filter_for_aggregation(
        self: T,
        inputs: Dict[str, Any],
        fields_names_for_regex: Tuple[str, ...] = tuple(),
        fields_names_for_range: Tuple[str, ...] = tuple(),
        fields_names_for_in: Tuple[str, ...] = tuple(),
        search_field_name: str = None,
        fields_names_for_search: Tuple[str, ...] = tuple(),
    ) -> tuple[dict, dict]:
        first_filter_inputs = dict()
        last_filter_inputs = dict()
        for key, value in inputs.items():
            if value:
                if key == search_field_name:
                    last_filter_inputs[key] = value

                elif self.field_separator in key:
                    if key.startswith(self.field_separator) or key.endswith(
                        self.field_separator
                    ):
                        # use for non-nested fields like count or average
                        last_filter_inputs[key.replace(self.field_separator, "")] = (
                            value
                        )
                    else:
                        last_filter_inputs[key.replace(self.field_separator, ".")] = (
                            value
                        )

                else:
                    first_filter_inputs[key] = value

        first_filter = self.prepare_filter(
            inputs=first_filter_inputs,
            fields_names_for_regex=fields_names_for_regex,
            fields_names_for_range=fields_names_for_range,
            fields_names_for_in=fields_names_for_in,
        )

        last_filter = self.prepare_filter(
            inputs=last_filter_inputs,
            fields_names_for_regex=fields_names_for_regex,
            fields_names_for_range=fields_names_for_range,
            fields_names_for_in=fields_names_for_in,
            search_field_name=search_field_name,
            fields_names_for_search=fields_names_for_search,
        )

        return first_filter, last_filter
