import pytest
import pytest_asyncio
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from utilsbeanie.utilsbeanie import UtilsBeanie
from tests.sample_document import SampleDoc, SampleDocWithUniquePid



@pytest_asyncio.fixture(
    scope="function",
    autouse=True,
)
async def initialize_beanie():
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    await init_beanie(
        database=client.test_db,
        document_models=[SampleDoc, SampleDocWithUniquePid],
    )


@pytest.fixture(scope="module")
def utils_beanie():
    return UtilsBeanie(
        document=SampleDoc,
        field_separator="__",
        )

@pytest.fixture(scope="module")
def utils_beanie_unique_pid():
    return UtilsBeanie(
        document=SampleDocWithUniquePid,
        field_separator="__",
        )
