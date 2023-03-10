import psycopg2
from psycopg2.extras import RealDictCursor
from config import settings

conn = psycopg2.connect(host={settings.database_hostname},user={settings.database_username},database={settings.database_name},
password={settings.database_password},cursor_factory=RealDictCursor)

cursor = conn.cursor()