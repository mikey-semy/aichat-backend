from typing import AsyncGenerator
from app.core.dependencies.connections.http import HttpClient

async def get_session() -> AsyncGenerator[HttpClient, None]:
    client = HttpClient()
    await client.connect()
    yield client
    await client.close()
