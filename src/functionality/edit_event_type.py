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
        # Add database query to fetch available event types
        select_query = "SELECT event_type FROM event_types WHERE user_id = %s"
        cursor.execute(select_query, (user_id,))
        event_types = cursor.fetchall()

        # Check if there are event types for the user
        if event_types:
            event_type_names = [event[0] for event in event_types]
            await channel.send("List of your available event types are: " + ", ".join(event_type_names))

            await channel.send("Please enter the event type to be edited")
            event_msg = await client.wait_for("message", check=check)
            event_type = event_msg.content

            # Check if the specified event type exists for the user
            if event_type in event_type_names:
                while True:
                    await channel.send("Please enter the new details for the event type in the following format:\n"
                                       "New Event Type Name\n"
                                       "New Start Time (in hh:mm am/pm format)\n"
                                       "New End Time (in hh:mm am/pm format)\n\nFor Example,\nStudy\n01:00 pm\n02:00 pm"
                                       )

                    # Wait for user input for the new details
                    new_details_msg = await client.wait_for("message", check=check)
                    new_details = new_details_msg.content.strip()
                    new_details_array = re.split("\s", new_details)
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

