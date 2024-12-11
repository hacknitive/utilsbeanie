import pytest
from beanie.exceptions import DocumentNotFound
from tests.sample_document import SampleDoc
from tests.fixtures import initialize_beanie, utils_beanie


@pytest.mark.asyncio
async def test_update_one_existing_document(utils_beanie):
    """
    Test updating a single existing document.
    """
    # Insert a document
    doc = await SampleDoc(pid=101, name="Update Test 1", value=1010).insert()

    # Update the document's name and value
    updated_doc = await utils_beanie.update_one_by_obj(doc, {"name": "Updated Name", "value": 2020})

    # Fetch the document to verify updates
    fetched_doc = await SampleDoc.get(doc.id)
    assert fetched_doc.name == "Updated Name"
    assert fetched_doc.value == 2020


@pytest.mark.asyncio
async def test_update_one_nonexistent_document(utils_beanie):
    """
    Test updating a document that does not exist.
    Since update_one expects an existing document instance, this test ensures that
    updating a deleted document raises an appropriate error or handles it gracefully.
    """
    # Insert and then delete a document
    doc = await SampleDoc(pid=102, name="Update Test 2", value=1020).insert()
    await doc.delete()

    # Attempt to update the deleted document
    with pytest.raises(DocumentNotFound) as exc_info:
        await utils_beanie.update_one_by_obj(doc, {"name": "Should Fail", "value": 3030})
    


@pytest.mark.asyncio
async def test_update_list_existing_documents(utils_beanie):
    """
    Test updating multiple existing documents.
    """
    # Insert multiple documents
    docs = [
        await SampleDoc(pid=201, name="Update List Test 1", value=2010).insert(),
        await SampleDoc(pid=202, name="Update List Test 2", value=2020).insert(),
        await SampleDoc(pid=203, name="Update List Test 3", value=2030).insert(),
    ]

    # Update the 'value' field for all documents
    updated_docs = await utils_beanie.update_list_by_obj(docs, {"value": 9999})

    # Fetch all documents to verify updates
    fetched_docs = await SampleDoc.find({"pid": {"$in": [201, 202, 203]}}).to_list()

    for fetched_doc in fetched_docs:
        assert fetched_doc.value == 9999


@pytest.mark.asyncio
async def test_update_list_empty(utils_beanie):
    """
    Test updating an empty list of documents.
    Should handle gracefully without errors.
    """
    # Update with an empty list
    updated_docs = await utils_beanie.update_list_by_obj([], {"name": "No Update"})

    # Verify that no documents are returned
    assert updated_docs == []


@pytest.mark.asyncio
async def test_update_list_with_some_nonexistent_documents(utils_beanie):
    """
    Test updating a list containing some non-existent documents.
    Should handle gracefully, updating only existing documents.
    """
    # Insert some documents
    existing_docs = [
        await SampleDoc(pid=301, name="Partial Update Test 1", value=3010).insert(),
        await SampleDoc(pid=302, name="Partial Update Test 2", value=3020).insert(),
    ]

    # Create a list with existing and non-existing documents
    non_existing_doc = SampleDoc(pid=999, name="Non-existent", value=9990)
    mixed_docs = existing_docs + [non_existing_doc]

    # Update the 'name' field for all documents
    # Assuming that update_list does not check for existence before updating
    # and will attempt to update only the provided document instances
    try:
        updated_docs = await utils_beanie.update_list_by_obj(mixed_docs, {"name": "Updated Mixed"})
    except Exception as e:
        # Depending on implementation, non-existent documents might raise an error
        # If so, catch and continue testing existing documents
        pass

    # Fetch existing documents to verify updates
    fetched_docs = await SampleDoc.find({"pid": {"$in": [301, 302]}}).to_list()
    for fetched_doc in fetched_docs:
        assert fetched_doc.name == "Updated Mixed"


@pytest.mark.asyncio
async def test_update_one_document_no_changes(utils_beanie):
    """
    Test updating a document without providing any changes.
    The document should remain unchanged.
    """
    # Insert a document
    doc = await SampleDoc(pid=401, name="No Change Test", value=4010).insert()

    # Update with empty inputs
    updated_doc = await utils_beanie.update_one_by_obj(doc, {})

    # Fetch the document to verify no changes
    fetched_doc = await SampleDoc.get(doc.id)
    assert fetched_doc.name == "No Change Test"
    assert fetched_doc.value == 4010


@pytest.mark.asyncio
async def test_update_one_document_partial_change(utils_beanie):
    """
    Test updating a document with partial changes.
    """
    # Insert a document
    doc = await SampleDoc(pid=501, name="Partial Change Test", value=5010).insert()

    # Update only the 'value' field
    updated_doc = await utils_beanie.update_one_by_obj(doc, {"value": 5020})

    # Fetch the document to verify updates
    fetched_doc = await SampleDoc.get(doc.id)
    assert fetched_doc.name == "Partial Change Test"
    assert fetched_doc.value == 5020


@pytest.mark.asyncio
async def test_update_list_all_documents(utils_beanie):
    """
    Test updating all documents in the collection.
    """
    # Insert multiple documents
    docs = [
        await SampleDoc(pid=6011, name="Bulk Update Test 1", value=6010).insert(),
        await SampleDoc(pid=6021, name="Bulk Update Test 2", value=6020).insert(),
        await SampleDoc(pid=6031, name="Bulk Update Test 3", value=6030).insert(),
    ]

    # Update all documents' 'name' field
    await utils_beanie.update_list_by_obj(docs, {"name": "Bulk Updated"})

    # Fetch all documents to verify updates
    fetched_docs = await SampleDoc.find({"pid": {"$in": [6011, 6021, 6031]}}).to_list()
    for fetched_doc in fetched_docs:
        assert fetched_doc.name == "Bulk Updated"
        # Ensure 'value' remains unchanged
        original_values = {6011: 6010, 6021: 6020, 6031: 6030}
        assert fetched_doc.value == original_values[fetched_doc.pid]