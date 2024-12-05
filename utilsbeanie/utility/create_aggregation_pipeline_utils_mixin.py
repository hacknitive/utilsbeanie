from typing import (
    Any,
    Dict,
    Type,
    Literal,
    Protocol,
    runtime_checkable,
    TypeVar,
    Generic,
)

from pydantic import BaseModel


@runtime_checkable
class CreateAggregationPipeLineUtilsMixinProtocol(Protocol):
    field_separator: str = "__"


T = TypeVar("T", bound=CreateAggregationPipeLineUtilsMixinProtocol)


class CreateAggregationPipeLineUtilsMixin(Generic[T]):
    
    def create_aggregation_pipeline(
        self,
        attributes: (
            tuple[tuple[str, Type[BaseModel]], ...] | None | tuple[dict[str, Any], ...]
        ),
        final_projection: Type[BaseModel] | dict[str, Literal[0, 1]] = None,
    ) -> list[dict]:
        aggregation_pipeline = list()

        if attributes:
            for attribute_i in attributes:
                if isinstance(attribute_i, dict):
                    lookup_from = attribute_i["lookup_from"]
                    lookup_local_field = attribute_i["lookup_local_field"]
                    lookup_foreign_field = attribute_i["lookup_foreign_field"]
                    lookup_as = attribute_i["lookup_as"]
                    projection_fields = self.prepare_projection_fields(
                        projection=attribute_i["projection_model"],
                    )
                    unwind = attribute_i.get("unwind", True)

                elif isinstance(attribute_i, tuple):
                    lookup_from = attribute_i[0]
                    lookup_local_field = f"{attribute_i[0]}_pid"
                    lookup_foreign_field = "pid"
                    lookup_as = f"{attribute_i[0]}_obj"
                    projection_fields = self.prepare_projection_fields(
                        projection=attribute_i[1]
                    )
                    unwind = True

                aggregation_pipeline.append(
                    {
                        "$lookup": {
                            "from": lookup_from,
                            "localField": lookup_local_field,
                            "foreignField": lookup_foreign_field,
                            "as": lookup_as,
                            "pipeline": [{"$project": projection_fields}],
                        }
                    },
                )

                if unwind:
                    aggregation_pipeline.append(
                        {
                            "$unwind": {
                                "path": f"${lookup_as}",
                                "preserveNullAndEmptyArrays": True,
                            }
                        }
                    )

        aggregation_pipeline.append(
            {"$project": self.prepare_projection_fields(projection=final_projection)}
        )
        return aggregation_pipeline

    @staticmethod
    def prepare_projection_fields(
        projection: Type[BaseModel] | Dict[str | Literal[0, 1], Any] | None
    ) -> Dict[str | Literal[0, 1], Any]:
        if isinstance(projection, dict):
            return projection

        elif issubclass(projection, BaseModel):
            return {"_id": 0, **{i: 1 for i in projection.model_fields.keys()}}
        return {"_id": 0}
