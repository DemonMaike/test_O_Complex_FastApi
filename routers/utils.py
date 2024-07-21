from geopy import Nominatim
from geopy.adapters import AioHTTPAdapter
from geopy.geocoders import Nominatim
import httpx
from pydantic import Json
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.city import city


async def get_coords(looking_city: str) -> tuple[float]:
    """ Func for coordinates of city, return (latitude, logitude) """
    async with Nominatim(
        user_agent="test_app",
        adapter_factory=AioHTTPAdapter,
    ) as geolocator:
        location = await geolocator.geocode(f"{looking_city}")

    return (location.latitude, location.longitude)


async def get_weather_of_day(latitude: float, longitude: float) -> Json | None:
    """ Get weather from open-meteo on current day. """
    url = f'https://api.open-meteo.com/v1/forecast?latitude={ \
        latitude}&longitude={longitude}&hourly=temperature_2m'

    async with httpx.AsyncClient() as client:
        result = await client.get(url)
        if result.status_code == 200:
            return result.json()


async def get_or_create_city(session: AsyncSession, city_name: str):
    city_name = city_name.lower()
    result = await session.execute(select(city).where(city.c.name == city_name))
    target = result.fetchone()

    if target:
        query = city.update().where(city.c.name == city_name).values(counter=city.c.counter + 1)
    else:
        query = city.insert().values(name=city_name, counter=1)

    await session.execute(query)
    await session.commit()