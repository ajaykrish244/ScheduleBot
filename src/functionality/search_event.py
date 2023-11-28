from functionality.shared_functions import add_event_to_file, connect_to_database
from Event import Event
from datetime import datetime, timedelta

async def search_event_by_name(ctx, event_name):
    # Connect to the database
    db_connection = connect_to_database()

    # Initialize the result variable
    event_exists = False

    # Create a cursor for database operations
    cursor = db_connection.cursor()

    try:
        # Use a parameterized query to prevent SQL injection
        query = "SELECT * FROM event WHERE name = %s"
        cursor.execute(query, (event_name,))

        # Fetch the result
        result = cursor.fetchone()

        if result:
            # If the event is found, set event_exists to True
            event_exists = True

    except Exception as e:
        print(f"Error while searching for event: {e}")
        # Log the error or handle it as needed

    finally:
        # Close the cursor and database connection in a finally block
        cursor.close()
        db_connection.close()

    return event_exists
