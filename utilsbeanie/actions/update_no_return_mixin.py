from typing import (
    Dict,
)

from beanie import (
    PydanticObjectId,
    Document,
    UpdateResponse,
)


class UpdateNoReturnMixin:

    async def update_list_by_filter(
        self,
        filter_: Dict,
        inputs: dict,
    ) -> Document:
        """This function do not return the updated obj. Only update result will be returned!"""
        return await self.document.find(filter_).update({"$set": inputs})

    async def update_one_by_filter(
        self,
        filter_: Dict,
        inputs: dict,
    ) -> Document:
        """This function do not return the updated obj. Only update result will be returned!"""
        return await self.document.find_one(filter_).update({"$set": inputs})

    async def update_one_by_id(
        self,
        id_: PydanticObjectId,
        inputs: dict,
    ) -> UpdateResponse:
        """This function do not return the updated obj. Only update result will be returned!"""
        return await self.document.find_one({"id": id_}).update({"$set": inputs})
    
    async def update_one_by_pid(
        self,
        pid: int | str,
        inputs: dict,
    ) -> UpdateResponse:
        """This function do not return the updated obj. Only update result will be returned!"""
        return await self.document.find_one({"pid": pid}).update({"$set": inputs})
    
