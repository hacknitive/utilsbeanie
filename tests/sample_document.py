from beanie import Document


# Define a Sample Document
class SampleDoc(Document):
    pid: int
    name: str
    value: int

    class Settings:
        name = "sample_docs"