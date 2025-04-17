import mysql.connector
from mysql.connector import Error
import time

def connect(query, data):
    conn = None
    max_retries = 3
    retry_delay = 2  # seconds
    
    for attempt in range(max_retries):
        try:
            print(f"Attempt {attempt + 1} to connect to database...")
            # Establish connection to MySQL
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="employee_db",
                connection_timeout=10,
                autocommit=True  # Enable autocommit
            )

            # Check if the connection was successful
            if conn.is_connected():
                print("Connection established successfully.")
                print(f"Executing query: {query}")
                print(f"With data: {data}")

                # Create a cursor object to interact with the database
                cursor = conn.cursor(buffered=True)

                # Execute the query
                cursor.execute(query, data)

                # If it's a SELECT query, fetch and return results
                if query.lower().strip().startswith("select"):
                    results = cursor.fetchall()
                    print(f"Query results: {results}")
                    cursor.close()
                    return results if results else []  # Return empty list if no results

                # If it's an INSERT/UPDATE/DELETE query, commit the changes
                else:
                    conn.commit()
                    cursor.close()
                    return True

        except Error as e:
            print(f"Database Error: {e}")
            print(f"Error Code: {e.errno}")
            print(f"SQL State: {e.sqlstate}")
            print(f"Error Message: {e.msg}")
            
            if attempt < max_retries - 1:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print("Max retries reached. Connection failed.")
                return False
                
        finally:
            # Ensure that the connection is closed
            if conn and conn.is_connected():
                conn.close()
                print("Connection closed.")

    return False

