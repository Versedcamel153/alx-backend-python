import mysql.connector

def stream_users_in_batches(batch_size):
    """Yields batches of users from the database."""
    connection = mysql.connector.connect(
        host="localhost",
        user="your_username",
        password="your_password",
        database="ALX_prodev"
    )
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")

    while True:
        batch = cursor.fetchmany(batch_size)
        if not batch:
            break
        yield batch

    cursor.close()
    connection.close()

def batch_processing(batch_size):
    """Processes batches to filter users over age 25 and yields them one by one."""
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user["age"] > 25:
                yield user  # <-- 🔥 Correct: use yield instead of print
    return