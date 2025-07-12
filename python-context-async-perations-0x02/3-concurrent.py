import asyncio
import aiosqlite

DB_FILE = 'users.db'

# Fetch all users
async def async_fetch_users():
    async with aiosqlite.connect(DB_FILE) as db:
        async with db.execute("SELECT * FROM users") as cursor:
            results = await cursor.fetchall()
            print("[All Users]")
            for row in results:
                print(row)
            return results

# Fetch users older than 40
async def async_fetch_older_users():
    async with aiosqlite.connect(DB_FILE) as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            results = await cursor.fetchall()
            print("\n[Users Older Than 40]")
            for row in results:
                print(row)
            return results

# Run both queries concurrently
async def fetch_concurrently():
    await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

# Kick off the event loop
if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
