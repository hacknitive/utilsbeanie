# UtilsBeanie

![PyPI][]
![License][]
![Python Version][]
![Build Status][]
![Coverage][]

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage Examples](#usage-examples)
  - [Initializing Beanie](#initializing-beanie)
  - [CRUD Operations](#crud-operations)
  - [Advanced Queries](#advanced-queries)
- [API Reference](#api-reference)
  - [Mixins](#mixins)
    - [DeleteMixin](#deletemixin)
    - [ExistMixin](#existmixin)
    - [FetchSimpleMixin](#fetchsimplemixin)
    - [InsertMixin](#insertmixin)
    - [UpdateByObjMixin](#updatebyobjmixin)
    - [UpdateNoReturnMixin](#updatenoreturnmixin)
    - [UpdateWithReturnMixin](#updatewithreturnmixin)
    - [FetchByAggregationPipelineMixin](#fetchbyaggregationpipelinemixin)
    - [FetchByGroupByAggregationPipelineMixin](#fetchbygroubyaaggregationpipelinemixin)
- [Configuration](#configuration)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)
- [Acknowledgments](#acknowledgments)

## Overview

**UtilsBeanie** is a comprehensive and ready-to-use wrapper for the [Beanie ODM](https://roman-right.github.io/beanie/) (Object Document Mapper). It streamlines repetitive tasks, providing a robust foundation for interacting with MongoDB in Python applications. Designed with modularity and extensibility in mind, UtilsBeanie simplifies CRUD operations, advanced querying, and version management, making it an invaluable tool for developers seeking efficiency and reliability.

## Features

- **Modular Mixins**: Easily extend your Beanie documents with a variety of mixins for common operations.
- **Automatic Versioning**: Scripts to manage version increments and Git operations seamlessly.
- **Comprehensive CRUD**: Simplified methods for Create, Read, Update, and Delete operations.
- **Advanced Querying**: Support for aggregation pipelines, group-by operations, and more.
- **Type Safety**: Extensive use of type hints and static analysis for robust and maintainable code.
- **Testing and Coverage**: Integrated testing framework with high coverage support.
- **CI/CD Integration**: Scripts and configurations ready for continuous integration and deployment.

## Installation

You can install UtilsBeanie via `pip` once it's published on PyPI. For the development version, clone the repository and install it manually.

### Via PyPI

```bash
pip install utilsbeanie
```

### From Source

```bash
git clone https://github.com/hacknitive/utilsbeanie.git
cd utilsbeanie
pip install .
```

## Quick Start

Here’s a brief example to get you started with UtilsBeanie.

### 1. Define Your Document

```python
from beanie import Document
from utilsbeanie.utilsbeanie import UtilsBeanie

class User(Document, UtilsBeanie):
    name: str
    email: str
    age: int

    class Settings:
        name = "users"
```

### 2. Initialize Beanie

```python
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from utilsbeanie.engine import Engin

async def init():
    engine = Engin(
        host="localhost",
        port=27017,
        database="test_db",
        username=None,
        password=None,
        authdb=None,
        connection_string=None,
    )
    connection, database = engine.create_connection_string(
        host="localhost",
        port=27017,
        database="test_db",
        username=None,
        password=None,
        authdb=None,
    )
    await UtilsBeanie.init_beanie(
        connection_string=connection,
        database=database,
        list_of_documents_pathes=[User],
    )

asyncio.run(init())
```

### 3. Perform CRUD Operations

```python
import asyncio

async def main():
    # Create a new user
    user = await User.insert_one_by_incremental_pid({
        "name": "John Doe",
        "email": "john.doe@example.com",
        "age": 30
    })
    print(f"Inserted User: {user}")

    # Fetch a user by PID
    fetched_user = await User.fetch_one_by_pid(user.pid)
    print(f"Fetched User: {fetched_user}")

    # Update a user
    updated_user = await User.update_one_by_pid(user.pid, {"age": 31})
    print(f"Updated User: {updated_user}")

    # Delete a user
    await User.delete_one_by_pid(user.pid)
    print("User deleted.")

asyncio.run(main())
```

## Usage Examples

### Initializing Beanie

Utilize the `Engin` class to create and manage your MongoDB connection.

```python
from motor.motor_asyncio import AsyncIOMotorClient
from utilsbeanie.engine import Engin

engine = Engin(
    host="localhost",
    port=27017,
    database="mydatabase",
    username="myuser",
    password="mypassword",
    authdb="admin",
    connection_string=None,
)

connection_string, database = engine.create_connection_string(
    host=engine.host,
    port=engine.port,
    database=engine.database,
    username=engine.username,
    password=engine.password,
    authdb=engine.authdb,
)

await UtilsBeanie.init_beanie(
    connection_string=connection_string,
    database=database,
    list_of_documents_pathes=[User, Order, Product],
)
```

### CRUD Operations

#### Create

```python
new_user = await User.insert_one_by_incremental_pid({
    "name": "Alice",
    "email": "alice@example.com",
    "age": 25
})
print(new_user)
```

#### Read

```python
# Fetch by PID
user = await User.fetch_one_by_pid(1001)
print(user)

# Fetch by Filter
users = await User.fetch_list_by_filter({"age": {"$gte": 21}})
for user in users:
    print(user)
```

#### Update

```python
# Update with return
updated_user = await User.update_one_by_pid(1001, {"age": 26})
print(updated_user)

# Update without return
await User.update_one_by_pid(1001, {"age": 27})
```

#### Delete

```python
await User.delete_one_by_pid(1001)
print("User deleted.")
```

### Advanced Queries

#### Aggregation Pipeline

```python
pipeline = [
    {"$match": {"age": {"$gte": 20}}},
    {"$group": {"_id": "$age", "count": {"$sum": 1}}},
    {"$sort": {"_id": 1}}
]

results = await User.fetch_by_aggregation_pipeline(pipeline)
for result in results:
    print(result)
```

#### Group By Aggregation

```python
group_by_fields = ["age"]

counts = await User.fetch_by_group_by_aggregation_pipeline(
    aggregation_pipeline=[],
    inputs={},
    group_by_on=group_by_fields
)
print(counts)
```

## API Reference

### Mixins

UtilsBeanie provides a suite of mixins to extend the functionality of your Beanie documents. Below is a brief overview of each mixin:

#### DeleteMixin

Provides methods for deleting documents.

- **Methods**:
  - `delete_list_by_filter(filter: Dict)`: Delete multiple documents matching the filter.
  - `delete_one_by_filter(filter: Dict)`: Delete a single document matching the filter.
  - `delete_one_by_id(id: PydanticObjectId)`: Delete a document by its Object ID.
  - `delete_one_by_pid(pid: str | int)`: Delete a document by its PID.

#### ExistMixin

Offers methods to check the existence of documents.

- **Methods**:
  - `is_one_item_absent_by_filter(filter: Dict, raise_on_existence: bool, exception_creator_func: Callable) -> bool`
  - `is_one_item_absent_by_id(id: PydanticObjectId, raise_on_existence: bool, exception_creator_func: Callable) -> bool`
  - `is_one_item_absent_by_pid(pid: str | int, raise_on_existence: bool, exception_creator_func: Callable) -> bool`
  - `is_one_item_exist_by_filter(filter: Dict, fetch_links: bool, raise_on_absence: bool, exception_creator_func: Callable) -> bool`
  - `is_one_item_exist_by_id(id: PydanticObjectId, raise_on_absence: bool, exception_creator_func: Callable) -> bool`
  - `is_one_item_exist_by_pid(pid: str | int, raise_on_absence: bool, exception_creator_func: Callable) -> bool`

#### FetchSimpleMixin

Provides basic fetching methods.

- **Methods**:
  - `fetch_one_by_id(document_id: Any) -> Document`
  - `fetch_one_by_pid(pid: str | int) -> Optional[Document]`
  - `fetch_one_by_filter(filter: Dict) -> Optional[Document]`
  - `fetch_list_by_filter(filter: Dict) -> List[Document]`
  - `fetch_list_by_filter_with_pagination(filter: Dict) -> Dict`
  - `fetch_count(filter: Dict) -> int`

#### InsertMixin

Facilitates inserting documents.

- **Methods**:
  - `insert_one_without_pid(inputs: Dict) -> Document`
  - `insert_one_by_epoch_pid(inputs: Dict) -> Document`
  - `insert_one_by_incremental_pid(inputs: Dict) -> Document`

#### UpdateByObjMixin

Enables updating documents by object.

- **Methods**:
  - `update_list(objs: List[Document], inputs: Dict) -> List[Document]`
  - `update_one(obj: Document, inputs: Dict) -> Document`

#### UpdateNoReturnMixin

Updates documents without returning them.

- **Methods**:
  - `update_list_by_filter(filter: Dict, inputs: Dict) -> Document`
  - `update_one_by_filter(filter: Dict, inputs: Dict) -> Document`
  - `update_one_by_id(id: PydanticObjectId, inputs: Dict) -> UpdateResponse`
  - `update_one_by_pid(pid: str | int, inputs: Dict) -> UpdateResponse`

#### UpdateWithReturnMixin

Updates documents and returns the updated document.

- **Methods**:
  - `update_one_by_filter_with_return(filter: Dict, inputs: Dict) -> Document`
  - `update_one_by_id(document_id: Any, inputs: Dict) -> Document`
  - `update_one_by_pid(pid: str | int, inputs: Dict) -> Document`
  - `update_list_by_filter(filter: Dict, inputs: Dict) -> List[Document]`

#### FetchByAggregationPipelineMixin

Handles fetching documents using aggregation pipelines.

- **Methods**:
  - `fetch_by_aggregation_pipeline(aggregation_pipeline: List[Dict]) -> List[Dict]`
  - `fetch_by_aggregation_pipeline_with_pagination(...) -> Dict`

#### FetchByGroupByAggregationPipelineMixin

Supports group-by operations within aggregation pipelines.

- **Methods**:
  - `fetch_by_group_by_aggregation_pipeline(...) -> Dict`
  - `fetch_by_group_by_aggregation_pipeline_with_pagination(...) -> Dict`

### Utility Classes

#### AggregationMixin

- **Methods**:
  - `build_aggregation_pipeline(attributes: Tuple, final_projection: Type[BaseModel] | Dict) -> List[Dict]`
  - `prepare_projection_fields(projection: Type[BaseModel] | Dict | None) -> Dict`

#### HelperMixin

- **Methods**:
  - `prepare_skip_limit(...) -> Dict`
  - `prepare_skip_limit_for_aggregation(...) -> List[Dict]`
  - `convert_order_by_to_sort_for_aggregation(...) -> List`

## Configuration

UtilsBeanie leverages environment variables and configuration files to manage settings securely and efficiently. Below is an example of how to set up your configuration.

### MongoDB Connection

You can configure your MongoDB connection using the `Engin` class.

```python
from utilsbeanie.engine import Engin

engine = Engin(
    host="localhost",
    port=27017,
    database="mydatabase",
    username="myuser",
    password="mypassword",
    authdb="admin",
    connection_string=None,  # If you prefer to use a connection URI directly
)

connection_string, database = engine.create_connection_string(
    host=engine.host,
    port=engine.port,
    database=engine.database,
    username=engine.username,
    password=engine.password,
    authdb=engine.authdb,
)
```

### Version Management

UtilsBeanie includes scripts for automatic versioning. Ensure that you have the necessary Git configuration and that your scripts are executable.

- **Make Scripts Executable**:

    ```bash
    chmod +x automatic_git_status_add_commit_push.sh
    chmod +x automatic_patch_versioning.sh
    ```

- **Running Version Scripts**:

    ```bash
    ./automatic_patch_versioning.sh
    ```

## Testing

UtilsBeanie emphasizes robust testing to ensure reliability. Follow these steps to run the test suite and check coverage.

### Prerequisites

Ensure that you have the development dependencies installed.

```bash
pip install -r requirements-test.txt
```

### Running Tests

Use `pytest` to run the test suite.

```bash
pytest
```

### Checking Coverage

Generate a coverage report using `coverage.py`.

```bash
coverage run -m pytest
coverage report
coverage html  # Generates an HTML report
```

## Contributing

We welcome contributions from the community! Below are guidelines to help you get started.

### How to Contribute

1. **Fork the Repository**: Click the "Fork" button on the repository page.

2. **Clone Your Fork**:

    ```bash
    git clone https://github.com/your-username/utilsbeanie.git
    cd utilsbeanie
    ```

3. **Create a New Branch**:

    ```bash
    git checkout -b feature/your-feature-name
    ```

4. **Make Your Changes**: Implement your feature or fix.

5. **Commit Your Changes**:

    ```bash
    git commit -m "Add feature X"
    ```

6. **Push to Your Fork**:

    ```bash
    git push origin feature/your-feature-name
    ```

7. **Create a Pull Request**: Submit a pull request describing your changes.

### Code Style

- Follow PEP 8 guidelines.
- Use `black` for code formatting.
- Ensure all new code is covered by tests.

### Reporting Issues

If you encounter any issues or have feature requests, please open an issue in the [GitHub Issues](https://github.com/hacknitive/utilsbeanie/issues) section.

### Code Review

All pull requests will be reviewed by the maintainers. Ensure your code passes all tests and follows the project's style guidelines.

## License

This project is licensed under the [MIT License](./LICENSE). You are free to use, modify, and distribute it as per the terms of the license.

## Contact

For any inquiries or support, please contact:

- **Author**: Reza 'Sam' Aghamohammadi (Hacknitive)
- **Email**: [hacknitive@gmail.com](mailto:hacknitive@gmail.com)
- **GitHub**: [https://github.com/hacknitive](https://github.com/hacknitive)

## Acknowledgments

- [Beanie ODM](https://roman-right.github.io/beanie/) for providing a powerful asynchronous ODM for MongoDB.
- [Motor](https://motor.readthedocs.io/en/stable/) for asynchronous MongoDB driver.
- [Pydantic](https://pydantic-docs.helpmanual.io/) for data validation and settings management.
- [Setuptools](https://setuptools.readthedocs.io/en/latest/) and [Wheel](https://wheel.readthedocs.io/en/stable/) for packaging tools.
- The open-source community for providing invaluable resources and support.

---

Thank you for using **UtilsBeanie**! We hope it enhances your development workflow and project efficiency. Feel free to contribute and share your feedback to help us improve further.