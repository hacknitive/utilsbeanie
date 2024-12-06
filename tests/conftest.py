import asyncio
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from tests.sample_document import SampleDoc


async def clean_db():
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    await init_beanie(
        database=client.test_db,
        document_models=[SampleDoc],
    )
    await SampleDoc.find().delete()


async def need_to_be_run():
    await clean_db()


def pytest_sessionstart(session) -> None:
    asyncio.run(need_to_be_run())
