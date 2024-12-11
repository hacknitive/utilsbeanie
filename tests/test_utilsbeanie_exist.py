import pytest
from tests.sample_document import SampleDoc
from tests.fixtures import initialize_beanie, utils_beanie

@pytest.mark.asyncio
async def test_is_one_item_absent_by_filter_exists(utils_beanie):
    # Insert a document
    await SampleDoc(pid=10, name="Exist Test", value=1000).insert()

    # Check if the item is absent (should be False)
    is_absent = await utils_beanie.is_one_item_absent_by_filter({"pid": 10})
    assert not is_absent

@pytest.mark.asyncio
async def test_is_one_item_absent_by_filter_not_exists(utils_beanie):
    # Ensure no document with pid=999 exists
    is_absent = await utils_beanie.is_one_item_absent_by_filter({"pid": 999})
    assert is_absent

@pytest.mark.asyncio
async def test_is_one_item_exist_by_filter_exists(utils_beanie):
    # Insert a document
    await SampleDoc(pid=20, name="Exist Test 2", value=2000).insert()

    # Check if the item exists (should be True)
    exists = await utils_beanie.is_one_item_exist_by_filter({"pid": 20})
    assert exists

@pytest.mark.asyncio
async def test_is_one_item_exist_by_filter_not_exists(utils_beanie):
    # Ensure no document with pid=888 exists
    exists = await utils_beanie.is_one_item_exist_by_filter({"pid": 888})
    assert not exists

@pytest.mark.asyncio
async def test_is_one_item_absent_by_id_exists(utils_beanie):
    # Insert a document
    doc = await SampleDoc(pid=30, name="Exist Test 3", value=3000).insert()

    # Check if the item is absent by ID (should be False)
    is_absent = await utils_beanie.is_one_item_absent_by_id(doc.id)
    assert not is_absent

@pytest.mark.asyncio
async def test_is_one_item_absent_by_id_not_exists(utils_beanie):
    # Use a random ObjectId (ensure it's not in the database)
    non_existent_id = "64b0c1f4f1a4f5c8b0d5e6f7"  # Example of a valid ObjectId
    is_absent = await utils_beanie.is_one_item_absent_by_id(non_existent_id)
    assert is_absent

@pytest.mark.asyncio
async def test_is_one_item_exist_by_id_exists(utils_beanie):
    # Insert a document
    doc = await SampleDoc(pid=40, name="Exist Test 4", value=4000).insert()

    # Check if the item exists by ID (should be True)
    exists = await utils_beanie.is_one_item_exist_by_id(doc.id)
    assert exists

@pytest.mark.asyncio
async def test_is_one_item_exist_by_id_not_exists(utils_beanie):
    # Use a random ObjectId (ensure it's not in the database)
    non_existent_id = "64b0c1f4f1a4f5c8b0d5e6f7"  # Example of a valid ObjectId
    exists = await utils_beanie.is_one_item_exist_by_id(non_existent_id)
    assert not exists

@pytest.mark.asyncio
async def test_is_one_item_absent_by_pid_exists(utils_beanie):
    # Insert a document
    await SampleDoc(pid=50, name="Exist Test 5", value=5000).insert()

    # Check if the item is absent by pid (should be False)
    is_absent = await utils_beanie.is_one_item_absent_by_pid(50)
    assert not is_absent

@pytest.mark.asyncio
async def test_is_one_item_absent_by_pid_not_exists(utils_beanie):
    # Ensure no document with pid=777 exists
    is_absent = await utils_beanie.is_one_item_absent_by_pid(777)
    assert is_absent

@pytest.mark.asyncio
async def test_is_one_item_exist_by_pid_exists(utils_beanie):
    # Insert a document
    await SampleDoc(pid=60, name="Exist Test 6", value=6000).insert()

    # Check if the item exists by pid (should be True)
    exists = await utils_beanie.is_one_item_exist_by_pid(60)
    assert exists

@pytest.mark.asyncio
async def test_is_one_item_exist_by_pid_not_exists(utils_beanie):
    # Ensure no document with pid=666 exists
    exists = await utils_beanie.is_one_item_exist_by_pid(666)
    assert not exists

@pytest.mark.asyncio
async def test_is_one_item_absent_by_filter_with_raise(utils_beanie):
    # Insert a document
    await SampleDoc(pid=70, name="Exist Test 7", value=7000).insert()

    # Define an exception creator function
    def exception_creator(document, filter_, method_name):
        return ValueError(f"Item exists in {document.Settings.name} with filter {filter_}.")

    # Attempt to check absence with raising exception
    with pytest.raises(ValueError) as exc_info:
        await utils_beanie.is_one_item_absent_by_filter(
            {"pid": 70},
            raise_on_existence=True,
            exception_creater_func=exception_creator
        )
    
    assert "Item exists in sample_docs with filter {'pid': 70}." in str(exc_info.value)

@pytest.mark.asyncio
async def test_is_one_item_exist_by_filter_with_raise(utils_beanie):
    # Ensure no document with pid=555 exists

    # Define an exception creator function
    def exception_creator(document, filter_, method_name):
        return ValueError(f"Item does not exist in {document.Settings.name} with filter {filter_}.")

    # Attempt to check existence with raising exception
    with pytest.raises(ValueError) as exc_info:
        await utils_beanie.is_one_item_exist_by_filter(
            {"pid": 555},
            raise_on_absence=True,
            exception_creater_func=exception_creator
        )
    
    assert "Item does not exist in sample_docs with filter {'pid': 555}." in str(exc_info.value)