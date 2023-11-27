from functionality.shared_functions import add_event_to_file, connect_to_database
from Event import Event
from datetime import datetime, timedelta


async def quick_schedule(ctx, event_type):
    """
    Schedules an event of the specified type within the next 24 hours if available.
    
    Args:
        ctx (discord.ext.commands.Context): Discord context object
        event_type (str): Type of event to schedule
    
    Returns:
        None
    """
    current_time = datetime.now()
    next_24_hours = current_time + timedelta(days=1)
    user_id = ctx.author.id
    channel = ctx.channel

    start_time, end_time = get_preferred_hours(event_type, user_id)

    if start_time is not None and end_time is not None:
        # Check if the time slot is available
        if is_time_slot_available(next_24_hours, next_24_hours + timedelta(hours=(end_time.hour - start_time.hour)), user_id):
            # Schedule the event
            formatted_start_time = start_time.strftime("%H:%M:%S")
            formatted_end_time = end_time.strftime("%H:%M:%S")
            message = f"Scheduling '{event_type}' event from {formatted_start_time} to {formatted_end_time} within the next 24 hours."
            await channel.send(message)
            
            # Add your code to actually schedule the event (insert into the database, etc.)
            current_event = Event(name=event_type, start_date=next_24_hours, end_date=next_24_hours + timedelta(hours=(end_time.hour - start_time.hour)),
                                  priority=1, event_type=event_type, description="", location="")
            add_event_to_file(user_id, current_event)
            
            success_message = f"Event '{event_type}' successfully scheduled!"
            await channel.send(success_message)
        else:
            error_message = f"Time slot is occupied for '{event_type}' within the next 24 hours. Unable to schedule."
            await channel.send(error_message)
    else:
        error_message = f"Event type '{event_type}' not found."
        await channel.send(error_message)


def get_preferred_hours(event_type, user_id):
    """
    Retrieves the preferred start and end time for a given event type and user.
    
    Args:
        event_type (str): Type of event
        user_id (str): Discord user ID
    
    Returns:
        tuple: Tuple containing start time and end time (or None, None if event type not found)
    """
    # Connect to MySQL database
    db_connection = connect_to_database()

    cursor = db_connection.cursor()

    try:
        # Select the start_time and end_time for the specified event type and user_id
        query = f"SELECT start_time, end_time FROM event_types WHERE event_type = '{event_type}' AND user_id = '{user_id}'"
        cursor.execute(query)

        # Fetch the result
        result = cursor.fetchone()

        if result:
            start_time, end_time = result
            return start_time, end_time
        else:
            return None, None  # Event type not found

    except Exception as e:
        print(f"Error: {e}")
        return None, None

    finally:
        # Close the cursor and connection
        cursor.close()
        db_connection.close()


def is_time_slot_available(start_date, end_date, user_id):
    """
    Checks if the specified time slot is available for scheduling an event.
    
    Args:
        start_date (datetime): Start date and time of the event
        end_date (datetime): End date and time of the event
        user_id (str): Discord user ID
    
    Returns:
        bool: True if the time slot is available, False otherwise
    """
    # Connect to MySQL database
    db_connection = connect_to_database()

    cursor = db_connection.cursor()

    try:
        # Query to check if there are any events within the specified time range
        query = (
            "SELECT * FROM EVENT "
            "WHERE user_id = %s AND ((start_date <= %s AND end_date >= %s) OR (start_date <= %s AND end_date >= %s))"
        )

        cursor.execute(query, (user_id, start_date, start_date, end_date, end_date))

        # Fetch all rows
        rows = cursor.fetchall()

        # If there are no rows, the time slot is available
        return len(rows) == 0
    finally:
        # Close the cursor and connection
        cursor.close()
        db_connection.close()

