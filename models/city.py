from sqlalchemy import Table, Integer, String, Column
from database import metadata


city = Table(
    'city',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('counter', Integer),
)