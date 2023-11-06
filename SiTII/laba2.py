import psycopg2
from sqlalchemy import create_engine, text
import xml.etree.ElementTree as ET
import os
import requests

incident_id = 169919
username = 'postgres'
password = '123'
host = 'localhost'
port = '5432'
mydatabase = 'db1'
DATABASE_URL = f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{mydatabase}"


engine = create_engine(DATABASE_URL)
conn = engine.connect()
result = conn.execute(text(f"select * from sitii_lr2_incidents where id = '{incident_id}'"))
for n in result:
    print(n)
conn.close()

