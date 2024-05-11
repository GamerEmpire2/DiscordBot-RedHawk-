import sqlite3

# Function to create tables if they don't exist
def create_tables():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        discriminator TEXT NOT NULL
    )
    """)
    # Add more tables as needed

# Function to insert data into the users table
def add_user(username, discriminator):
    cursor.execute("INSERT INTO users (username, discriminator) VALUES (?, ?)", (username, discriminator))
    conn.commit()

# Function to fetch all users from the database
def get_all_users():
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    return rows

# Connect to SQLite database
conn = sqlite3.connect('./discordbot.db')
cursor = conn.cursor()

# Execute commands
create_tables()  # Create tables if they don't exist

# Don't forget to commit the changes and close the connection
conn.commit()
conn.close()
