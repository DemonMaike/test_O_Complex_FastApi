import pytest
from httpx import AsyncClient
from ..main import app
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")
timezone_str = "UTC"

@pytest.mark.asyncio
async def test_root_page():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

@pytest.mark.asyncio
async def test_weather_forecast():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/get_weather", data={"city": "London"})
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "London" in response.text