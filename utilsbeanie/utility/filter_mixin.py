from re import escape
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
class FilterMixinProtocol(Protocol): ...


T = TypeVar("T", bound=FilterMixinProtocol)


class FilterMixin(Generic[T]):
    def prepare_filter(
        self,
        inputs: Dict[str, Any],
        fields_names_for_regex: Tuple[str, ...] = tuple(),
        fields_names_for_range: Tuple[str, ...] = tuple(),
        fields_names_for_in: Tuple[str, ...] = tuple(),
        search_field_name: str = None,
        fields_names_for_search: Tuple[str, ...] = tuple(),
    ) -> dict:
        filter_ = []

        filter_.extend(
            self.prepare_filter_for_regex_fields(
                fields_names=fields_names_for_regex,
                inputs=inputs,
            )
        )

        filter_.extend(
            self.prepare_filter_for_range_fields(
                fields_names=fields_names_for_range,
                inputs=inputs,
            )
        )

        filter_.extend(
            self.prepare_filter_for_in_fields(
                fields_names=fields_names_for_in,
                inputs=inputs,
            )
        )

        if search_field_name:
            filter_.append(
                self.prepare_filter_for_search_field(
                    search_field_name=search_field_name,
                    fields_to_search_on=fields_names_for_search,
                    inputs=inputs,
                )
            )

        if not filter_:
            return {}

        if len(filter_) == 1:
            return filter_[0]

        return {"$and": filter_}

    @staticmethod
    def prepare_filter_for_boolean_fields(
        field_names: tuple[str],
        kwargs: dict,
    ):
        filter_ = []
        for field_name in field_names:
            if kwargs[field_name] is not None:
                filter_.append({field_name: kwargs[field_name]})

        return filter_

    @staticmethod
    def prepare_filter_for_in_fields(
        fields_names: tuple[str, ...],
        inputs: dict,
    ):
        filter_ = []    
        for field_name in fields_names:

            if inputs.get(field_name):
                filter_.append({field_name: {"$in": list(set(inputs[field_name]))}})

        return filter_

    @staticmethod
    def prepare_filter_for_range_fields(
        fields_names: tuple[str, ...],
        inputs: dict,
    ):
        filter_ = []

        for field_name in fields_names:
            from_ = field_name + "_from"
            to = field_name + "_to"
            include_null = field_name + "_include_null"

            sub_filter = dict()
            or_filter = list()
            if inputs.get(from_) is not None:
                sub_filter["$gte"] = inputs[from_]

            if inputs.get(to) is not None:
                sub_filter["$lt"] = inputs[to]

            if sub_filter:
                or_filter.append({field_name: sub_filter})

            if inputs.get(include_null):
                or_filter.append({field_name: None})

            if or_filter:
                filter_.append({"$or": or_filter})

        return filter_

    @staticmethod
    def prepare_filter_for_regex_fields(
        fields_names: tuple[str, ...],
        inputs: dict,
    ):
        filter_ = []
        for field_name in fields_names:
            if inputs.get(field_name):
                subfilter = list()
                for i in set(inputs[field_name]):
                    subsubfilter = list()
                    for j in i.split(" "):
                        subsubfilter.append({field_name: {"$regex": escape(j)}})

                    if len(subsubfilter) > 1:
                        subfilter.append({"$and": subsubfilter})

                    else:
                        subfilter.append(subsubfilter[0])

                filter_.append({"$or": subfilter})

        return filter_

    @staticmethod
    def prepare_filter_for_search_field(
        search_field_name: str,
        fields_to_search_on: tuple[str, ...],
        inputs: dict,
    ):
        filter_ = []
        # {"$and": [{'title': {"$regex": /g/}}, {'title': {"$regex": /i/}}]}
        if inputs.get(search_field_name):

            split_value = list()
            for i in inputs[search_field_name]:
                split_value.extend(i.split())

            if split_value:
                search_filter = list()
                for i in split_value:
                    subfilter = list()
                    for field_name in fields_to_search_on:
                        subfilter.append({field_name: {"$regex": escape(i)}})

                    if len(subfilter) == 1:
                        search_filter.append(subfilter[0])

                    elif len(subfilter) > 1:
                        search_filter.append({"$or": subfilter})

                if search_filter:
                    filter_.append({"$and": search_filter})

        return filter_
