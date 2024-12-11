from typing import (
    Type,
    List,
)

from beanie import Document


class UpdateByObjMixin:
    @staticmethod
    async def update_list_by_obj(
        objs: List[Type[Document]],
        inputs: dict,
    ) -> List[Type[Document]]:
        for obj in objs:
            for attr, value in inputs.items():
                setattr(obj, attr, value)

            await obj.replace()

        return objs

    @staticmethod
    async def update_one_by_obj(
        obj: Type[Document] | Document,
        inputs: dict,
    ) -> Type[Document]:
        for attr, value in inputs.items():
            setattr(obj, attr, value)

        await obj.replace()

        return obj
