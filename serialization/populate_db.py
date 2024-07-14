import sqlite3

# Connect to the database (creates it if it doesn't exist)
conn = sqlite3.connect('your_database.db')

# Enable WAL mode
conn.execute('PRAGMA journal_mode=WAL')

# Create a cursor
cursor = conn.cursor()

# Create your tables here
# For example:
cursor.execute('''CREATE TABLE IF NOT EXISTS your_table
                  (id INTEGER PRIMARY KEY, name TEXT, value INTEGER)''')

# Commit the changes and close the connection
conn.commit()
conn.close()