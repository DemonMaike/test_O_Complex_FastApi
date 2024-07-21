from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from .utils import get_coords, get_weather_of_day, get_or_create_city
from zoneinfo import ZoneInfo

router = APIRouter()
templates = Jinja2Templates(directory='templates/')
timezone_str = 'Europe/Moscow' # нужно будет получать от пользователя динамически

@router.get('/', response_class=HTMLResponse)
async def root_page(request: Request):

    return templates.TemplateResponse('base.html', {'request': request})


@router.post('/get_weather')
async def weather_forecast(request: Request, city: str = Form(...),
 session: AsyncSession = Depends(get_async_session)):

    latitude, longitude = await get_coords(city)
    data = await get_weather_of_day(latitude, longitude)

    now = datetime.now(ZoneInfo(timezone_str))
    weather_data = {datetime.fromisoformat(time).replace(tzinfo=ZoneInfo(timezone_str)): \
     temp for time, temp in zip(data['hourly']['time'], data['hourly']['temperature_2m'])}

    closest_time = min(weather_data.keys(), key=lambda t: abs(t - now))
    start_time = closest_time - timedelta(hours=3)
    end_time = closest_time + timedelta(hours=3)

    selected_weather = {time: temp for time, temp in weather_data.items() \
     if start_time <= time <= end_time}

    await get_or_create_city(session, city)

    return templates.TemplateResponse('base.html', {'request': request,'city_name': city, 'forecast': selected_weather})
