import time
from psycopg_pool import ConnectionPool
from psycopg.rows import dict_row

DB_DSN = "host=localhost dbname=fastapi user=postgres password=@Piyush#123"

# Try until DB is ready
while True:
    try:
        pool = ConnectionPool(
            conninfo=DB_DSN,
            min_size=1,
            max_size=10,
            max_idle=300,
            timeout=30,
            kwargs={"row_factory": dict_row}
        )
        print("✅ Database connection pool established")
        break
    except Exception as error:
        print("❌ DB connection failed:", error)
        time.sleep(2)
