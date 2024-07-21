from typing import Dict
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from models.city import city

router = APIRouter()

@router.get('/count', response_model=Dict[str, int])
async def count_city_weather(session: AsyncSession = Depends(get_async_session)):
    
    result = await session.execute(select(city.c.name, city.c.counter))
    cities = result.fetchall()
    response = {row[0]: row[1] for row in cities}

    return response