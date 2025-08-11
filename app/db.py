import time
from psycopg_pool import ConnectionPool
from psycopg.rows import dict_row

# Database connection string (DSN) containing host, database name, user, and password.
# This will be used by psycopg to connect to PostgreSQL.
DB_DSN = "host=localhost dbname=fastapi user=postgres password=@Piyush#123"

"""
This script sets up a PostgreSQL connection pool using psycopg3's `ConnectionPool`.
A connection pool maintains a set of open connections that can be reused, improving
performance by avoiding repeated connection creation.

Key points about the connection pool:
- `min_size`: Minimum number of connections kept ready in the pool.
- `max_size`: Maximum number of simultaneous connections allowed.
- `max_idle`: Maximum time (in seconds) an unused connection is kept before closing.
- `timeout`: How long to wait when trying to get a connection before raising an error.
- `row_factory=dict_row`: Ensures query results are returned as dictionaries instead of tuples.

The `while True` loop ensures that if the database isn't ready (e.g., during service startup),
the app will keep retrying until a connection is successfully established.
"""

while True:
    try:
        # Create the connection pool
        pool = ConnectionPool(
            conninfo=DB_DSN,                  # PostgreSQL connection parameters
            min_size=1,                        # Keep at least 1 open connection ready
            max_size=10,                       # Allow up to 10 simultaneous connections
            max_idle=300,                      # Close unused connections after 5 minutes
            timeout=30,                        # Max wait time to get a connection from pool
            kwargs={"row_factory": dict_row}   # Fetch rows as dictionaries
        )

        # If creation is successful, log the success and stop retrying
        print("✅ Database connection pool established")
        break

    except Exception as error:
        # If connection fails, print the error and retry after a short delay
        print("❌ DB connection failed:", error)
        time.sleep(2)  # Wait before retrying to avoid spamming connection attempts
