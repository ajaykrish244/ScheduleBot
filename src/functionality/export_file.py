import os
import csv
import discord

from functionality.shared_functions import load_key, decrypt_file, encrypt_file


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

    # key = load_key(user_id)
    # decrypt_file(key, os.path.expanduser("~/Documents") + "/ScheduleBot/Event/" + user_id + ".csv")

    # await channel.send(file=discord.File(os.path.expanduser("~/Documents") + "/ScheduleBot/Event/" + user_id + ".csv"))

    # encrypt_file(key, os.path.expanduser("~/Documents") + "/ScheduleBot/Event/" + user_id + ".csv")