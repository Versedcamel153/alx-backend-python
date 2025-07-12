import time
import sqlite3
import functools

# ---- DB connection handler ----
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            result = func(conn, *args, **kwargs)
            return result
        finally:
            conn.close()
    return wrapper

# ---- Retry on transient failure ----
def retry_on_failure(retries=3, delay=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            while attempt < retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempt += 1
                    print(f"[RETRY] Attempt {attempt} failed: {e}")
                    if attempt == retries:
                        print("[RETRY] Max retries reached. Giving up.")
                        raise
                    time.sleep(delay)
        return wrapper
    return decorator

# ---- DB operation with retry logic ----
@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

# ---- Run it ----
users = fetch_users_with_retry()
print(users)
