import os
import re
import csv
from pathlib import Path
from types import TracebackType
from functionality.shared_functions import load_key, encrypt_file, decrypt_file
import mysql.connector
from functionality.shared_functions import connect_to_database


async def delete_event_type(ctx, client):
    """
    Function: delete_event_type
    Description: Walks a user through deleting existing event types in the calendar database
    Input:
        ctx - Discord context window
        client - Discord bot user
    Output:
        - An existing event type is deleted from the user's calendar in the database
        - A message sent to the context saying an event type was successfully deleted
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

        # Query the database to fetch the list of available event types for the user
        select_query = "SELECT event_type FROM event_types WHERE user_id = %s"
        cursor.execute(select_query, (user_id,))
        event_types = cursor.fetchall()

        # Check if there are event types for the user
        if event_types:
            event_type_names = [event[0] for event in event_types]
            await channel.send("List of your available event types are: " + ", ".join(event_type_names))

            await channel.send("Please enter the event type to be deleted")
            event_msg = await client.wait_for("message", check=check)
            event_type = event_msg.content

            # Check if the specified event type exists for the user
            if event_type in event_type_names:
                # Delete the event type from the database
                delete_query = "DELETE FROM event_types WHERE user_id = %s AND event_type = %s"
                cursor.execute(delete_query, (user_id, event_type))
                db_connection.commit()
                await channel.send("Event type " + event_type + " has been deleted.")
            else:
                await channel.send("Event type does not exist.")
        else:
            await channel.send("You have not created any event types yet.")

    except mysql.connector.Error as error:
        print(f"Error: {error}")
    finally:
        # Close the cursor and database connection
        if db_connection.is_connected():
            cursor.close()
            db_connection.close()

    # Check if an event type was deleted and send a confirmation message
    if event_type:
        await channel.send("Event type " + event_type + " has been deleted from your calendar.")

# Example usage:
# Call delete_event_type with ctx and client when a user wants to delete an event type
