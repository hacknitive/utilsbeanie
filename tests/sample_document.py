from typing import Annotated

from beanie import Document, Indexed


class SampleDoc(Document):
    pid: int
    name: str
    value: int

    class Settings:
        name = "sample_docs"

class SampleDocWithUniquePid(Document):
    pid: Annotated[int, Indexed(unique=True)]
    name: str
    value: int

    class Settings:
        name = "sample_doc_with_unique_pid"