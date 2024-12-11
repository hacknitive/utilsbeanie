import pytest
from pymongo.errors import DuplicateKeyError
from tests.sample_document import SampleDoc, SampleDocWithUniquePid
from tests.fixtures import initialize_beanie, utils_beanie, utils_beanie_unique_pid

@pytest.mark.asyncio
async def test_update_one_by_filter_with_return_existing_document(utils_beanie):
    # Insert a document
    doc = await SampleDoc(pid=10, name="Original Name", value=100).insert()
    
    # Update fields
    update_fields = {"name": "Updated Name", "value": 200}
    
    # Perform the update
    updated_doc = await utils_beanie.update_one_by_filter_with_return({"pid": 10}, update_fields)
    
    # Check that the returned document is not None
    assert updated_doc is not None
    assert updated_doc.pid == 10
    assert updated_doc.name == "Updated Name"
    assert updated_doc.value == 200
    
    # Verify the actual change in the database
    fetched_doc = await SampleDoc.find_one({"pid": 10})
    assert fetched_doc.name == "Updated Name"
    assert fetched_doc.value == 200


@pytest.mark.asyncio
async def test_update_one_by_id_with_return_existing_document(utils_beanie):
    # Insert a document
    doc = await SampleDoc(pid=20, name="Original Name ID", value=300).insert()
    
    # Update fields
    update_fields = {"name": "Updated Name ID", "value": 400}
    
    # Perform the update by ID
    updated_doc = await utils_beanie.update_one_by_id_with_return(doc.id, update_fields)
    
    # Check that the returned document is not None
    assert updated_doc is not None
    assert updated_doc.pid == 20
    assert updated_doc.name == "Updated Name ID"
    assert updated_doc.value == 400
    
    # Verify the actual change in the database
    fetched_doc = await SampleDoc.get(doc.id)
    assert fetched_doc.name == "Updated Name ID"
    assert fetched_doc.value == 400

@pytest.mark.asyncio
async def test_update_one_by_pid_with_return_existing_document(utils_beanie):
    # Insert a document
    doc = await SampleDoc(pid=3054654, name="Original Name PID", value=500).insert()
    
    # Update fields
    update_fields = {"name": "Updated Name PID", "value": 600}
    
    # Perform the update by PID
    updated_doc = await utils_beanie.update_one_by_pid_with_return(3054654, update_fields)
    
    # Check that the returned document is not None
    assert updated_doc is not None
    assert updated_doc.pid == 3054654
    assert updated_doc.name == "Updated Name PID"
    assert updated_doc.value == 600
    
    # Verify the actual change in the database
    fetched_doc = await SampleDoc.find_one({"pid": 3054654})
    assert fetched_doc.name == "Updated Name PID"
    assert fetched_doc.value == 600

@pytest.mark.asyncio
async def test_update_list_by_filter_with_return_existing_documents(utils_beanie):
    # Insert multiple documents
    docs = [
        await SampleDoc(pid=40, name="List Update Test 1", value=700).insert(),
        await SampleDoc(pid=41, name="List Update Test 2", value=700).insert(),
        await SampleDoc(pid=42, name="List Update Test 3", value=700).insert(),
    ]
    
    # Update fields
    update_fields = {"value": 800}
    
    # Perform the update on all documents matching the filter
    updated_docs = await utils_beanie.update_list_by_filter_with_return({"value": 700}, update_fields)
    
    # Check that three documents were returned
    assert len(updated_docs) == 3
    
    for updated_doc in updated_docs:
        assert updated_doc.value == 800
    
    # Verify the actual changes in the database
    fetched_docs = await SampleDoc.find({"value": 800}).to_list()
    assert len(fetched_docs) == 3
    for doc in fetched_docs:
        assert doc.value == 800

@pytest.mark.asyncio
async def test_update_list_by_filter_with_return_partial_updates(utils_beanie):
    # Insert multiple documents
    docs = [
        await SampleDoc(pid=50, name="Partial Update Test 1", value=900).insert(),
        await SampleDoc(pid=51, name="Partial Update Test 2", value=900).insert(),
    ]
    
    # Update only the 'name' field
    update_fields = {"name": "Partially Updated"}
    
    # Perform the update on all documents matching the filter
    updated_docs = await utils_beanie.update_list_by_filter_with_return({"value": 900}, update_fields)
    
    # Check that two documents were returned
    assert len(updated_docs) == 2
    
    for updated_doc in updated_docs:
        assert updated_doc.name == "Partially Updated"
        assert updated_doc.value == 900  # Ensure 'value' remains unchanged
    
    # Verify the actual changes in the database
    fetched_docs = await SampleDoc.find({"value": 900}).to_list()
    assert len(fetched_docs) == 2
    for doc in fetched_docs:
        assert doc.name == "Partially Updated"
        assert doc.value == 900

@pytest.mark.asyncio
async def test_update_list_by_filter_with_return_nonexistent_documents(utils_beanie):
    # Attempt to update a list containing some non-existent documents
    # Assuming that update_list_by_filter_with_return only updates existing documents
    
    # Insert one document
    existing_doc = await SampleDoc(pid=6000001, name="Existing Update Test", value=1000).insert()
    
    # Define the filter to update both existing and non-existing documents
    update_filter = {"pid": {"$in": [6000001, 6000010]}}  # pid=999 does not exist
    update_fields = {"value": 1100}
    
    # Perform the update
    updated_docs = await utils_beanie.update_list_by_filter_with_return(update_filter, update_fields)
    
    # Check that only one document was returned and updated
    assert len(updated_docs) == 1
    assert updated_docs[0].pid == 6000001
    assert updated_docs[0].value == 1100
    
    # Verify the actual changes in the database
    fetched_doc = await SampleDoc.find_one({"pid": 6000001})
    assert fetched_doc.value == 1100
    fetched_nonexistent_doc = await SampleDoc.find_one({"pid": 6000010})
    assert fetched_nonexistent_doc is None

@pytest.mark.asyncio
async def test_update_one_by_filter_with_return_duplicate_key(utils_beanie_unique_pid):
    # Insert a document with a unique PID
    doc1 = await SampleDocWithUniquePid(pid=70, name="Original Unique", value=1000).insert()
    
    # Insert another document with a different PID
    doc2 = await SampleDocWithUniquePid(pid=71, name="Another Document", value=1100).insert()
    
    # Attempt to update doc2's PID to doc1's PID, which should raise DuplicateKeyError
    update_fields = {"pid": 70}
    
    with pytest.raises(DuplicateKeyError):
        await utils_beanie_unique_pid.update_one_by_filter_with_return({"pid": 71}, update_fields)

@pytest.mark.asyncio
async def test_update_one_by_filter_with_return_invalid_update_fields(utils_beanie):
    # Insert a document
    doc = await SampleDoc(pid=80, name="Invalid Update Test", value=1200).insert()
    
    # Attempt to update with invalid field (assuming 'nonexistent_field' does not exist)
    update_fields = {"nonexistent_field": "Invalid"}
    
    # Perform the update
    with pytest.raises(ValueError):
        updated_doc = await utils_beanie.update_one_by_filter_with_return({"pid": 80}, update_fields)


@pytest.mark.asyncio
async def test_update_one_by_filter_with_return_partial_field_updates(utils_beanie):
    # Insert a document
    doc = await SampleDoc(pid=90, name="Partial Field Update Test", value=1300).insert()
    
    # Update only the 'value' field
    update_fields = {"value": 1400}
    
    # Perform the update
    updated_doc = await utils_beanie.update_one_by_filter_with_return({"pid": 90}, update_fields)
    
    # Check that the returned document has the updated field
    assert updated_doc is not None
    assert updated_doc.value == 1400
    assert updated_doc.name == "Partial Field Update Test"
    
    # Verify the actual change in the database
    fetched_doc = await SampleDoc.find_one({"pid": 90})
    assert fetched_doc.value == 1400
    assert fetched_doc.name == "Partial Field Update Test"

@pytest.mark.asyncio
async def test_update_one_by_filter_with_return_raise_on_error(utils_beanie_unique_pid):
    # Insert two documents with unique PIDs
    doc1 = await SampleDocWithUniquePid(pid=100022, name="Unique PID Test 1", value=2000).insert()
    doc2 = await SampleDocWithUniquePid(pid=101022, name="Unique PID Test 2", value=2100).insert()
    
    # Define an exception creator function
    def exception_creator(document, filter_, method_name):
        return ValueError(f"Update failed in {document.Settings.name} with filter {filter_}.")
    
    # Attempt to update doc2's PID to doc1's PID, which should raise DuplicateKeyError and be caught as ValueError
    update_fields = {"pid": 100022}
    
    with pytest.raises(DuplicateKeyError):
        await utils_beanie_unique_pid.update_one_by_filter_with_return(
            {"pid": 101022},
            update_fields
        )

@pytest.mark.asyncio
async def test_update_one_by_filter_with_return_no_changes(utils_beanie):
    # Insert a document
    doc = await SampleDoc(pid=110, name="No Change Test", value=1500).insert()
    
    # Update with empty inputs
    update_fields = {}
    updated_doc = await utils_beanie.update_one_by_filter_with_return({"pid": 110}, update_fields)
    
    # Check that the returned document is the same as before
    assert updated_doc is not None
    assert updated_doc.pid == 110
    assert updated_doc.name == "No Change Test"
    assert updated_doc.value == 1500
    
    # Verify the actual change in the database remains unchanged
    fetched_doc = await SampleDoc.find_one({"pid": 110})
    assert fetched_doc.name == "No Change Test"
    assert fetched_doc.value == 1500

@pytest.mark.asyncio
async def test_update_list_by_filter_with_return_with_duplicate_keys(utils_beanie_unique_pid):
    # Insert two documents with unique PIDs
    doc1 = await SampleDocWithUniquePid(pid=13001, name="Unique Update Test 0", value=2200).insert()
    doc1 = await SampleDocWithUniquePid(pid=12001, name="Unique Update Test 1", value=2200).insert()
    doc2 = await SampleDocWithUniquePid(pid=12101, name="Unique Update Test 2", value=2300).insert()
    
    # Attempt to update both documents to have the same PID, causing a DuplicateKeyError
    update_filter = {"pid": {"$in": [12001, 12101]}}
    update_fields = {"pid": 13001}
    
    with pytest.raises(DuplicateKeyError):
        await utils_beanie_unique_pid.update_list_by_filter_with_return(update_filter, update_fields)
    
    # Verify that no documents were updated due to the error
    fetched_doc1 = await SampleDocWithUniquePid.find_one({"pid": 12001})
    fetched_doc2 = await SampleDocWithUniquePid.find_one({"pid": 12101})
    assert fetched_doc1.pid == 12001
    assert fetched_doc2.pid == 12101

@pytest.mark.asyncio
async def test_update_list_by_filter_with_return_unique_pid(utils_beanie_unique_pid):
    # Insert documents with unique PIDs
    doc1 = await SampleDocWithUniquePid(pid=13000, name="Unique Update Test A", value=240000).insert()
    doc2 = await SampleDocWithUniquePid(pid=13100, name="Unique Update Test B", value=250000).insert()
    
    # Update fields
    update_fields = {"value": 260000}
    
    # Perform the update on all documents matching the filter
    updated_docs = await utils_beanie_unique_pid.update_list_by_filter_with_return({"value": {"$lt": 300000}}, update_fields)
    
    # Check that two documents were returned and updated
    assert len(updated_docs) >= 2
    for updated_doc in updated_docs:
        assert updated_doc.value == 260000
    
    # Verify the actual changes in the database
    fetched_docs = await SampleDocWithUniquePid.find({"value": 260000}).to_list()
    assert len(fetched_docs) >= 2
    for doc in fetched_docs:
        assert doc.value == 260000