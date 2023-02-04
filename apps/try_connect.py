import psycopg2
from psycopg2.extras import RealDictCursor

conn = psycopg2.connect(host="localhost",user="postgres",database="fastAPI",
password="16062016JustifyMy",cursor_factory=RealDictCursor)

cursor = conn.cursor()