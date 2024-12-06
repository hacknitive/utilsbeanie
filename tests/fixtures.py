import pytest
import pytest_asyncio
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from utilsbeanie.utilsbeanie import UtilsBeanie
from tests.sample_document import SampleDoc



@pytest_asyncio.fixture(
    scope="function",
    autouse=True,
)
async def initialize_beanie():
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    await init_beanie(
        database=client.test_db,
        document_models=[SampleDoc],
    )


@pytest.fixture(scope="module")
def utils_beanie():
    return UtilsBeanie(
        document=SampleDoc,
        field_separator="__",
        )
