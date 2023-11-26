import re
from datetime import datetime
from functionality.shared_functions import connect_to_database

async def edit_event_type(ctx, client):
    """
    Function: edit_event_type
    Description: Walks a user through editing an existing event type in the calendar database
    Input:
        ctx - Discord context window
        client - Discord bot user
    Output:
        - An existing event type is edited in the user's calendar in the database
        - A message sent to the context saying an event type was successfully edited
    """
    channel = await ctx.author.create_dm()
    user_id = str(ctx.author.id)
    event_type = None

    def check(m):
        return m.content is not None and m.channel == channel and m.author == ctx.author

    try:
        # Establish a connection to the MySQL database
        db_connection = connect_to_database()
        # Create a cursor object to execute SQL commands
        cursor = db_connection.cursor()
    except Exception as error:
        print(f"Error: {error}")
    finally:
        # Close the cursor and database connection
        if db_connection.is_connected():
            cursor.close()
            db_connection.close()

    # Check if an event type was edited and send a confirmation message
    if event_type:
        await channel.send(f"Event type {event_type} has been edited in your calendar.")

