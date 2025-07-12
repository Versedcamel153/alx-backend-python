import time
import sqlite3
import functools

query_cache = {}

# Decorator to open and close DB connection
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

# Decorator to cache query results based on the query string
def cache_query(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        # Try to extract query string
        query = kwargs.get("query")
        if not query and len(args) > 0:
            query = args[0] if isinstance(args[0], str) else args[1]

        # Use query as cache key
        if query in query_cache:
            print(f"[CACHE HIT] Returning cached result for: {query}")
            return query_cache[query]
        
        print(f"[CACHE MISS] Executing query: {query}")
        result = func(conn, *args, **kwargs)
        query_cache[query] = result
        return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")
print(users)

# Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")
print(users_again)
