from urllib.parse import quote_plus

from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie as _init_beanie
from beanie import Document


class Engin:
    def __init__(
        self,
        host: str,
        port: int | str,
        database: str | None,
        username: str | None,
        password: str | None,
        authdb: str | None,
        connection_string: str | None,
    ) -> None:
        self.host = host
        self.port = port
        self.database = database
        self.username = username
        self.password = password
        self.authdb = authdb
        self.connection_string = connection_string

    @staticmethod
    async def init_beanie(
        connection_string: str, 
        database: str, 
        list_of_documents_pathes: list[str | Document]
    ) -> None:
        client = AsyncIOMotorClient(connection_string)

        await _init_beanie(
            database=client[database],
            document_models=list_of_documents_pathes,
        )

    @staticmethod
    def create_connection_string(
        host: str,
        port: int | str,
        database: str | None,
        username: str | None,
        password: str | None,
        authdb: str | None,
    ) -> tuple[str, str|None]:
        connection_string = "mongodb://"

        if username:
            connection_string += f"{quote_plus(username)}:{quote_plus(password)}@"

        connection_string += f"{host}:{port}/"

        if database:
            connection_string += f"{database}"

        if authdb:
            connection_string += f"?authSource={authdb}"

        return connection_string, database
