from functionality.shared_functions import add_event_to_file, connect_to_database
from Event import Event
from datetime import datetime, timedelta


async def quick_schedule(ctx, event_type):
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
