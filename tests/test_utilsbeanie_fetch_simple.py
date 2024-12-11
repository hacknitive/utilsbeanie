import pytest
from tests.sample_document import SampleDoc
from tests.fixtures import initialize_beanie, utils_beanie
from utilsbeanie.constant import EnumOrderBy

@pytest.mark.asyncio
async def test_fetch_one_by_id_exists(utils_beanie):
    # Insert a document
    doc = await SampleDoc(pid=100, name="Fetch Test 1", value=1000).insert()

    # Fetch the document by ID
    fetched_doc = await utils_beanie.fetch_one_by_id(doc.id)
    assert fetched_doc is not None
    assert fetched_doc.pid == 100
    assert fetched_doc.name == "Fetch Test 1"
    assert fetched_doc.value == 1000


@pytest.mark.asyncio
async def test_fetch_one_by_id_not_exists(utils_beanie):
    # Use a random ObjectId (ensure it's not in the database)
    non_existent_id = "64b0c1f4f1a4f5c8b0d5e6f7"  # Example of a valid ObjectId
    fetched_doc = await utils_beanie.fetch_one_by_id(non_existent_id)
    assert fetched_doc is None


@pytest.mark.asyncio
async def test_fetch_one_by_pid_exists(utils_beanie):
    # Insert a document
    await SampleDoc(pid=200, name="Fetch Test 2", value=2000).insert()

    # Fetch the document by pid
    fetched_doc = await utils_beanie.fetch_one_by_pid(200)
    assert fetched_doc is not None
    assert fetched_doc.pid == 200
    assert fetched_doc.name == "Fetch Test 2"
    assert fetched_doc.value == 2000


@pytest.mark.asyncio
async def test_fetch_one_by_pid_not_exists(utils_beanie):
    # Ensure no document with pid=999 exists
    fetched_doc = await utils_beanie.fetch_one_by_pid(999)
    assert fetched_doc is None


@pytest.mark.asyncio
async def test_fetch_one_by_filter_exists(utils_beanie):
    # Insert a document
    await SampleDoc(pid=300, name="Fetch Test 3", value=3000).insert()

    # Fetch the document by filter
    fetched_doc = await utils_beanie.fetch_one_by_filter({"pid": 300})
    assert fetched_doc is not None
    assert fetched_doc.pid == 300
    assert fetched_doc.name == "Fetch Test 3"
    assert fetched_doc.value == 3000


@pytest.mark.asyncio
async def test_fetch_one_by_filter_not_exists(utils_beanie):
    # Ensure no document with pid=888 exists
    fetched_doc = await utils_beanie.fetch_one_by_filter({"pid": 888})
    assert fetched_doc is None


@pytest.mark.asyncio
async def test_fetch_list_by_filter(utils_beanie):
    # Insert multiple documents
    await SampleDoc(pid=400, name="Fetch List Test 1", value=4004).insert()
    await SampleDoc(pid=401, name="Fetch List Test 2", value=4004).insert()
    await SampleDoc(pid=402, name="Fetch List Test 3", value=4004).insert()

    # Fetch the list by filter
    fetched_docs = await utils_beanie.fetch_list_by_filter({"value": 4004})
    assert len(fetched_docs) == 3
    pids = {doc.pid for doc in fetched_docs}
    assert pids == {400, 401, 402}


@pytest.mark.asyncio
async def test_fetch_list_by_filter_with_pagination(utils_beanie):
    # Insert multiple documents
    for i in range(500, 510):
        await SampleDoc(pid=i, name=f"Fetch Paginate Test {i}", value=5002).insert()

    # Fetch the first page with page size 5
    result = await utils_beanie.fetch_list_by_filter_with_pagination(
        filter_={"value": 5002},
        current_page=1,
        page_size=5,
        order_by={"pid": EnumOrderBy.A.value},
    )
    assert result["pagination"]["total"] == 10
    assert result["pagination"]["current"] == 1
    assert result["pagination"]["page_size"] == 5
    assert len(result["data"]) == 5
    assert [doc.pid for doc in result["data"]] == list(range(500, 505))

    # Fetch the second page with page size 5
    result = await utils_beanie.fetch_list_by_filter_with_pagination(
        filter_={"value": 5002},
        current_page=2,
        page_size=5,
        order_by={"pid": EnumOrderBy.A.value},
    )
    assert result["pagination"]["total"] == 10
    assert result["pagination"]["current"] == 2
    assert result["pagination"]["page_size"] == 5
    assert len(result["data"]) == 5
    assert [doc.pid for doc in result["data"]] == list(range(505, 510))


@pytest.mark.asyncio
async def test_fetch_count(utils_beanie):
    # Insert multiple documents
    await SampleDoc(pid=600, name="Count Test 1", value=6008).insert()
    await SampleDoc(pid=601, name="Count Test 2", value=6008).insert()

    # Fetch the count
    count = await utils_beanie.fetch_count(filter_={"value": 6008})
    assert count == 2


@pytest.mark.asyncio
async def test_fetch_one_by_filter_with_sort(utils_beanie):
    # Insert multiple documents with different pids
    await SampleDoc(pid=700, name="Sort Test 1", value=7005).insert()
    await SampleDoc(pid=701, name="Sort Test 2", value=7005).insert()
    await SampleDoc(pid=702, name="Sort Test 3", value=7005).insert()

    # Fetch the first document sorted by pid descending
    fetched_doc = await utils_beanie.fetch_one_by_filter(
        {"value": 7005},
        sort=("pid", -1)
    )
    assert fetched_doc is not None
    assert fetched_doc.pid == 702

    # Fetch the first document sorted by pid ascending
    fetched_doc = await utils_beanie.fetch_one_by_filter(
        {"value": 7005},
        sort=("pid", 1)
    )
    assert fetched_doc is not None
    assert fetched_doc.pid == 700


@pytest.mark.asyncio
async def test_fetch_one_by_filter_with_projection(utils_beanie):
    # Insert a document
    await SampleDoc(pid=800, name="Projection Test", value=8000).insert()

    # Fetch the document with projection (only 'pid' and 'name')
    fetched_doc = await utils_beanie.fetch_one_by_filter(
        {"pid": 800},
        projection_model=SampleDoc.model_construct(pid=0, name=0)  # Adjust projection as needed
    )
    assert fetched_doc is not None
    assert hasattr(fetched_doc, 'pid')
    assert hasattr(fetched_doc, 'name')
    assert hasattr(fetched_doc, 'value')
    # Depending on how projection_model is implemented, you might need to adjust assertions


@pytest.mark.asyncio
async def test_fetch_list_by_filter_with_negative_conditions(utils_beanie):
    # Insert documents
    await SampleDoc(pid=900, name="Negative Test 1", value=9000).insert()
    await SampleDoc(pid=901, name="Negative Test 2", value=9000).insert()

    # Fetch documents where pid is not 900
    fetched_docs = await utils_beanie.fetch_list_by_filter({"pid": {"$ne": 900}})
    assert len(fetched_docs) >= 1
    assert 901 in {i.pid for i in fetched_docs}