from typing import (
    Type,
    List,
)

from beanie import Document


class UpdateByObjMixin:
    @staticmethod
    async def update_list(
        objs: List[Type[Document]],
        inputs: dict,
    ) -> List[Type[Document]]:
        for obj in objs:
            for attr, value in inputs.items():
                setattr(obj, attr, value)

            await obj.save()

        return objs

    @staticmethod
    async def update_one(
        obj: Type[Document] | Document,
        inputs: dict,
    ) -> Type[Document]:
        for attr, value in inputs.items():
            setattr(obj, attr, value)

        await obj.save()

        return obj
