import mysql.connector
import uuid

# Establish a connection to the MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="hbnb_dev",
    password="hbnb_dev_pwd",
    database="hbnb_dev_db"
)

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

# Define the SQL statement to insert a new row into the states table
sql = """
    INSERT INTO states (id, created_at, updated_at, name) 
    VALUES (%s, %s, %s, %s)
"""
# Generate a new UUID for the id column
id = str(uuid.uuid4())
values = (
    id,                                        # id
    "2022-04-19 08:00:00",                     # created_at
    "2022-04-19 08:00:00",                     # updated_at
    "New York"                                 # name
)

# Execute the SQL statement
cursor.execute(sql, values)

# Commit the transaction
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()
