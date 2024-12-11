import pytest
from beanie import Document
from beanie.odm.documents import PydanticObjectId
from pymongo.errors import DuplicateKeyError
from tests.sample_document import SampleDocWithUniquePid
from tests.fixtures import initialize_beanie, utils_beanie_unique_pid

@pytest.mark.asyncio
async def test_update_one_by_filter_no_return_existing_document(utils_beanie_unique_pid):
    # Insert a document
    doc = await SampleDocWithUniquePid(pid=10, name="Original Name", value=100).insert()
    
    # Update fields
    update_fields = {"name": "Updated Name", "value": 200}
    
    # Perform the update
    result = await utils_beanie_unique_pid.update_one_by_filter_no_return({"pid": 10}, update_fields)
    
    # Check the update result (modified_count should be 1)
    assert result.modified_count == 1
    
    # Verify the actual change in the database
    updated_doc = await SampleDocWithUniquePid.find_one({"pid": 10})
    assert updated_doc.name == "Updated Name"
    assert updated_doc.value == 200

@pytest.mark.asyncio
async def test_update_one_by_filter_no_return_nonexistent_document(utils_beanie_unique_pid):
    # Attempt to update a non-existent document
    update_fields = {"name": "Should Not Exist", "value": 999}
    result = await utils_beanie_unique_pid.update_one_by_filter_no_return({"pid": 999}, update_fields)
    
    # Check that no documents were modified
    assert result.modified_count == 0

@pytest.mark.asyncio
async def test_update_one_by_id_no_return_existing_document(utils_beanie_unique_pid):
    # Insert a document
    doc = await SampleDocWithUniquePid(pid=20, name="Original Name ID", value=300).insert()
    
    # Update fields
    update_fields = {"name": "Updated Name ID", "value": 400}
    
    # Perform the update by ID
    result = await utils_beanie_unique_pid.update_one_by_id_no_return(doc.id, update_fields)
    
    # Check the update result (modified_count should be 1)
    assert result.modified_count == 1
    
    # Verify the actual change in the database
    updated_doc = await SampleDocWithUniquePid.get(doc.id)
    assert updated_doc.name == "Updated Name ID"
    assert updated_doc.value == 400

@pytest.mark.asyncio
async def test_update_one_by_id_no_return_nonexistent_document(utils_beanie_unique_pid):
    # Generate a random ObjectId
    non_existent_id = PydanticObjectId()
    
    # Attempt to update a non-existent document by ID
    update_fields = {"name": "Should Not Exist ID", "value": 888}
    result = await utils_beanie_unique_pid.update_one_by_id_no_return(non_existent_id, update_fields)
    
    # Check that no documents were modified
    assert result.modified_count == 0

@pytest.mark.asyncio
async def test_update_one_by_pid_no_return_existing_document(utils_beanie_unique_pid):
    # Insert a document
    doc = await SampleDocWithUniquePid(pid=30, name="Original Name PID", value=500).insert()
    
    # Update fields
    update_fields = {"name": "Updated Name PID", "value": 600}
    
    # Perform the update by PID
    result = await utils_beanie_unique_pid.update_one_by_pid_no_return(30, update_fields)
    
    # Check the update result (modified_count should be 1)
    assert result.modified_count == 1
    
    # Verify the actual change in the database
    updated_doc = await SampleDocWithUniquePid.find_one({"pid": 30})
    assert updated_doc.name == "Updated Name PID"
    assert updated_doc.value == 600

@pytest.mark.asyncio
async def test_update_one_by_pid_no_return_nonexistent_document(utils_beanie_unique_pid):
    # Attempt to update a non-existent document by PID
    update_fields = {"name": "Should Not Exist PID", "value": 777}
    result = await utils_beanie_unique_pid.update_one_by_pid_no_return(999, update_fields)
    
    # Check that no documents were modified
    assert result.modified_count == 0

@pytest.mark.asyncio
async def test_update_list_by_filter_no_return_existing_documents(utils_beanie_unique_pid):
    # Insert multiple documents
    docs = [
        await SampleDocWithUniquePid(pid=4001, name="List Update Test 1", value=70001).insert(),
        await SampleDocWithUniquePid(pid=4101, name="List Update Test 2", value=70001).insert(),
        await SampleDocWithUniquePid(pid=4201, name="List Update Test 3", value=70001).insert(),
    ]
    
    # Update fields
    update_fields = {"value": 80001}
    
    # Perform the update on all documents matching the filter
    result = await utils_beanie_unique_pid.update_list_by_filter_no_return({"value": 70001}, update_fields)
    
    # Check the update result (modified_count should be 3)
    assert result.modified_count == 3
    
    # Verify the actual changes in the database
    updated_docs = await SampleDocWithUniquePid.find({"value": 80001}).to_list()
    assert len(updated_docs) == 3
    for doc in updated_docs:
        assert doc.value == 80001

@pytest.mark.asyncio
async def test_update_list_by_filter_no_return_no_matching_documents(utils_beanie_unique_pid):
    # Attempt to update with a filter that matches no documents
    update_fields = {"value": 900}
    result = await utils_beanie_unique_pid.update_list_by_filter_no_return({"value": 999}, update_fields)
    
    # Check that no documents were modified
    assert result.modified_count == 0

@pytest.mark.asyncio
async def test_update_one_by_filter_no_return_duplicate_key(utils_beanie_unique_pid):
    # Insert a document with a unique PID
    await SampleDocWithUniquePid(pid=50, name="Original Unique", value=1000).insert()
    
    # Attempt to update another document to have the same PID, causing a DuplicateKeyError
    update_fields = {"pid": 50}
    
    # Insert another document to update
    doc_to_update = await SampleDocWithUniquePid(pid=51, name="Another Document", value=1100).insert()
    
    with pytest.raises(DuplicateKeyError):
        await utils_beanie_unique_pid.update_one_by_filter_no_return({"pid": 51}, update_fields)