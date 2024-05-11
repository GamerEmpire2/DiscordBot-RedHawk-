import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('./discordbot.db')
cursor = conn.cursor()

# Execute SQL commands here (e.g., create tables, insert data, query data)

# Don't forget to commit the changes and close the connection
conn.commit()
conn.close()
