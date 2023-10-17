import re
import os
import csv
from datetime import datetime
from types import TracebackType
from event_type import event_type
# from functionality.shared_functions import create_type_directory, create_type_file
from functionality.shared_functions import decrypt_file, encrypt_file
from functionality.shared_functions import connect_to_database

async def create_event_type(ctx, client, event_msg):
    """
    Function:
        create_event_type
    Description:
        Walks a user through the creation of types of event or updating time range for existing event types
    Input:
        ctx - Discord context window
        client - Discord bot user
    Output:
        - A new event type added to the user's calendar file or the time range will be update for the existing event type
        - A message sent to the context saying an event type was successfully added or updated
    """
    print("i am in event type creation")
    channel = await ctx.author.create_dm()
    print(ctx.author.id)

    def check(m):
        return m.content is not None and m.channel == channel and m.author == ctx.author

    event_array = []
    # await channel.send("First give me the type of your event:")
    # event_msg = await client.wait_for("message", check=check)  # Waits for user input
    # event_msg = event_msg.content  # Strips message to just the text the user entered
    event_array.append(event_msg)
    await channel.send(
        "Now give me your perefered time range this event type.\n"
        + "Make sure you include 'am' or 'pm' so I know what is the range of your event, \n"
        + "Here is the format you should follow (Start is first, end is second):\n"
        + "hh:mm am/pm hh:mm am/pm"
    )

    time_range = False
    # A loop that keeps running until a user enters correct start and end time for their event type following the required format
    # Adds start and end time to the array if both are valid
    while not time_range:
        time_array = []
        msg_content = ""
        start_complete = False
        end_complete = True
        if ctx.message.author != client.user:
            # Waits for user input
            event_msg = await client.wait_for("message", check=check)
            # Strips message to just the text the user entered
            msg_content = event_msg.content
            # Splits response to prepare data to be appended to event_array
            time_array = re.split("\s", msg_content)

        try:
            start_time = datetime.strptime(
                time_array[0] + " " + time_array[1], "%I:%M %p"
            )
            start_complete = True
            print("Created start_time object: " + str(start_time))
        except Exception as e:
            print(e)
            await channel.send(
                "Looks like you didn't enter your start time correctly. Please re-enter your time.\n"
                + "Here is the format you should follow (Start is first, end is second):\n"
                + "hh:mm am/pm hh:mm am/pm"
            )
            start_complete = False
            continue

        # Tries to create the end_time datetime object
        try:
            end_time = datetime.strptime(time_array[2] + " " + time_array[3], "%I:%M %p")
            end_complete = True
            print("Created end_time object: " + str(end_time))
        except Exception as e:
            print(e)
            await channel.send(
                "Looks like you didn't enter your end time correctly. Please re-enter your time.\n"
                + "Here is the format you should follow (Start is first, end is second):\n"
                + "hh:mm am/pm hh:mm am/pm"
            )
            end_complete = False
            continue

        # Tries to create the end_time datetime object
        if end_time <= start_time:
            await channel.send(
                "Looks like your end time is before your start time. Please re-enter your time.\n"
                + "Here is the format you should follow (Start is first, end is second):\n"
                + "hh:mm am/pm hh:mm am/pm"
            )
            end_complete = False
            start_complete = False
            continue

        # If both datetime objects were successfully created, they get appended to the list and exits the while loop
        if start_complete and end_complete:
            print("Both time objects created")
            time_range = True
            event_array.append(start_time)
            event_array.append(end_time)

        # If both objects were unsuccessfully created, the bot notifies the user and the loop starts again
        else:
            await channel.send(
                "Make sure you follow this format(Start is first, end is second): mm/dd/yy hh:mm am/pm mm/dd/yy hh:mm am/pm"
            )
            time_array = []
            msg_content = ""

    # Tries to create an Event_type object from the user input
    try:

        current = event_type(event_array[0], event_array[1], event_array[2])

        # Establish a connection to the MySQL database
        db_connection = connect_to_database()

        # Create a cursor object to execute SQL commands
        cursor = db_connection.cursor()

        # Check if the user already exists in the database
        select_query = "SELECT COUNT(*) FROM event_types WHERE event_type = %s AND user_id = %s"
        cursor.execute(select_query, (current.event_name, ctx.author.id))
        count = cursor.fetchone()[0]

        if count > 0:
            # If the user exists, update the event
            update_query = "UPDATE event_types SET start_time = %s, end_time = %s WHERE event_type = %s AND user_id = %s"
            cursor.execute(update_query, (current.start_time, current.end_time, current.event_name, ctx.author.id))
        else:
            # If the user does not exist, insert a new event
            insert_query = "INSERT INTO event_types (event_type, start_time, end_time, user_id) VALUES (%s, %s, %s, %s)"
            cursor.execute(insert_query, (current.event_name, current.start_time, current.end_time, ctx.author.id))

        # Commit the changes to the database
        db_connection.commit()


        cursor.close()
        db_connection.close()


        return True

    except Exception as e:
        # Outputs an error message if the event type could not be created
        print(e)
        TracebackType.print_exc()
        await channel.send(
            "There was an error while adding this event type. Make sure your formatting is correct and try creating the event type again."
        )
        return False