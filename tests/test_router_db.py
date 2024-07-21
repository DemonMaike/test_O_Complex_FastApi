import pytest
from httpx import AsyncClient
from ..main import app

@pytest.mark.asyncio
async def test_count_city_weather():
    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        response = await ac.get("/count")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)