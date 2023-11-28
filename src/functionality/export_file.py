import os
import csv
import discord
from pathlib import Path
from src.functionality.shared_functions import read_event_file


async def export_file(ctx):
    """
    Function:
        export_file
    Description:
        Sends the user a CSV file containing their scheduled events.
    Input:
        ctx - Discord context window
    Output:
        - A CSV file sent to the context that contains a user's scheduled events.
    """

    channel = await ctx.author.create_dm()
    print(ctx.author.id)

    user_id = str(ctx.author.id)
    rows = read_event_file(user_id)

    if not os.path.exists(os.path.expanduser("../tmp/")):
        Path(os.path.expanduser("../tmp/")).mkdir(parents=True, exist_ok=True)

    with open("../tmp/"+user_id+".csv", "w+") as f:
        writer = csv.writer(f)
        writer.writerows(rows)
    
    await channel.send(file=discord.File(os.path.expanduser("../tmp/"+user_id+".csv")))