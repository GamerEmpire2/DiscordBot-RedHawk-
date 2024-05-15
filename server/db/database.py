import os
import sqlite3

def initialize_database():
    latest_version = get_latest_version()

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create the version table if it doesn't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS version (
        version INTEGER
    )
    """)

    # Get the current version
    cursor.execute("SELECT version FROM version")
    row = cursor.fetchone()
    current_version = row[0] if row else 0

    # Apply updates for each version greater than the current version
    for version in range(current_version + 1, latest_version + 1):
        update_database_to_version(cursor, version)

    conn.commit()
    conn.close()

def update_database_to_version(cursor, version):
    # Validate the version number
    if not isinstance(version, int) or version < 1:
        raise ValueError("Invalid version number")

    # Construct the filename
    filename = f'{migrations_path}/{version}.sql'

    # Read the SQL commands from the file
    with open(filename, 'r') as f:
        sql_commands = f.read()

    try:
        # Execute the database migration in a transaction in case of error
        cursor.execute('BEGIN TRANSACTION')
        cursor.executescript(sql_commands)
        cursor.execute('UPDATE version SET version = ?', (version,))
        cursor.execute('COMMIT')
        print(f"Database updated to version {version}")
    except sqlite3.Error as e:
        # An error occurred, rollback the transaction
        cursor.execute('ROLLBACK')
        print(f"Error updating database to version {version}: {e}")

    finally:
        conn.close()

def get_latest_version():
    # Get a list of all .sql files in the ./db/migrations directory
    files = os.listdir(migrations_path)

    # Extract the version numbers from the filenames
    versions = []
    for f in files:
        if f.endswith('.sql'):
            try:
                version = int(f.split('.')[0])
                versions.append(version)
            except ValueError:
                print(f"Warning: Ignoring file '{f}' because its name is not an integer.")

    # Return the highest version number
    return max(versions)

# Function to insert data into the users table
def add_user(username, email, discriminator, hashed_password, salt):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO users (username, email, discriminator, hashed_password, salt) 
        VALUES (?, ?, ?, ?, ?)
    """, (username, email, discriminator, hashed_password, salt))
    conn.commit()

# Function to fetch all users from the database
def get_all_users():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    return rows

# Execute commands
db_path = './database.db'
migrations_path = './migrations'
initialize_database()