import pytest
from tests.sample_document import SampleDoc
from tests.fixtures import initialize_beanie, utils_beanie


# Test delete_one_by_filter
@pytest.mark.asyncio
async def test_delete_one_by_filter(utils_beanie):
    # Insert a document
    await SampleDoc(pid=1, name="Delete Filter Test", value=100).insert()

    # Ensure the document exists
    assert await SampleDoc.find_one({"pid": 1}) is not None

    # Delete the document using filter
    await utils_beanie.delete_one_by_filter({"pid": 1})

    # Verify deletion
    deleted = await SampleDoc.find_one({"pid": 1})
    assert deleted is None

# Test delete_list_by_filter
@pytest.mark.asyncio
async def test_delete_list_by_filter(utils_beanie):
    # Insert multiple documents
    await SampleDoc(pid=2, name="Delete List Test 1", value=200).insert()
    await SampleDoc(pid=3, name="Delete List Test 2", value=300).insert()
    await SampleDoc(pid=4, name="Delete List Test 3", value=400).insert()

    # Ensure documents exist
    docs = await SampleDoc.find({"value": {"$gte": 200}}).to_list()
    assert len(docs) == 3

    # Delete documents using filter
    await utils_beanie.delete_list_by_filter({"value": {"$gte": 200}})

    # Verify deletion
    deleted_docs = await SampleDoc.find({"value": {"$gte": 200}}).to_list()
    assert len(deleted_docs) == 0

# Test delete_one_by_id
@pytest.mark.asyncio
async def test_delete_one_by_id(utils_beanie):
    # Insert a document
    doc = await SampleDoc(pid=5, name="Delete ID Test", value=500).insert()

    # Ensure the document exists
    assert await SampleDoc.get(doc.id) is not None

    # Delete the document by ID
    await utils_beanie.delete_one_by_id(doc.id)

    # Verify deletion
    deleted = await SampleDoc.get(doc.id)
    assert deleted is None

# Test delete_one_by_pid
@pytest.mark.asyncio
async def test_delete_one_by_pid(utils_beanie):
    # Insert a document
    await SampleDoc(pid=6, name="Delete PID Test", value=600).insert()

    # Ensure the document exists
    assert await SampleDoc.find_one({"pid": 6}) is not None

    # Delete the document by pid
    await utils_beanie.delete_one_by_pid(6)

    # Verify deletion
    deleted = await SampleDoc.find_one({"pid": 6})
    assert deleted is None

# Test delete_one_by_pid with non-existent pid
@pytest.mark.asyncio
async def test_delete_one_by_pid_nonexistent(utils_beanie):
    # Attempt to delete a non-existent pid
    await utils_beanie.delete_one_by_pid(999)

    # Verify that no document was deleted
    deleted = await SampleDoc.find_one({"pid": 999})
    assert deleted is None

# Test delete_one_by_filter_multiple_matches (should delete only one)
@pytest.mark.asyncio
async def test_delete_one_by_filter_multiple_matches(utils_beanie):
    # Insert multiple documents with the same value
    await SampleDoc(pid=7, name="Delete Multi Test 1", value=700).insert()
    await SampleDoc(pid=8, name="Delete Multi Test 2", value=700).insert()

    # Ensure both documents exist
    docs = await SampleDoc.find({"value": 700}).to_list()
    assert len(docs) == 2

    # Delete one document by filter
    await utils_beanie.delete_one_by_filter({"value": 700})

    # Verify that only one document is deleted
    remaining_docs = await SampleDoc.find({"value": 700}).to_list()
    assert len(remaining_docs) == 1

    # Clean up remaining document
    await SampleDoc.find_one({"pid": remaining_docs[0].pid}).delete()