import os
import sys
import pathlib
from dotenv import load_dotenv
from typing import Literal, Optional

import discord
from discord.components import SelectOption  # type: ignore
from discord.ext import commands  # type: ignore
from discord import ui, app_commands

from functionality.schedule import SchedModal
from functionality.edit_event_type import edit_event_type
from functionality.Delete_Event import delete_event
from functionality.GoogleEvent import get_events
from functionality.Google import connect_google
from functionality.import_file import import_file
from functionality.export_file import export_file
from functionality.DisplayFreeTime import get_free_time
from functionality.delete_event_type import delete_event_type
from functionality.FindAvailableTime import find_avaialbleTime
from functionality.delete_event_type import delete_event_type
from functionality.DisplayFreeTime import get_free_time
from functionality.export_file import export_file
from functionality.import_file import import_file
from functionality.Google import connect_google
from functionality.GoogleEvent import get_events
from functionality.Delete_Event import delete_event
from functionality.edit_event_type import edit_event_type
from functionality.quick_schedule import quick_schedule
from functionality.search_event import search_event_by_name
from functionality.schedule import SchedModal

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
print(TOKEN)

DCPREFIX = '/'
intents = discord.Intents.all()
# Creates the bot with a command prefix of '/'
bot = commands.Bot(command_prefix=DCPREFIX, intents=intents, )
# Removes the help command, so it can be created using Discord embed pages later
bot.remove_command("help")


# class my_modal(ui.Modal, title="Bot modal"):
#     answer=ui.TextInput(label="enter something", style=discord.TextStyle.short, placeholder="Yes")
#     async def on_submit(self, interaction: discord.Interaction):
#         await interaction.response.send_message("hello world")


# https://gist.github.com/AbstractUmbra/a9c188797ae194e592efe05fa129c57f#file-03-syncing_gotchas_and_tricks-md
@bot.command()
async def sync(ctx: commands.Context, spec: Optional[Literal["~", "*", "^"]] = None) -> None:
    """
    Synchronize commands between the global command tree and the current guild's command tree.

    Parameters:
    - ctx (commands.Context): The context of the command invocation.
    - spec (Optional[Literal["~", "*", "^"]]): Optional specifier for synchronization:
        - "~": Synchronize commands only within the current guild.
        - "*": Synchronize commands globally across all guilds.
        - "^": Clear all local guild commands before synchronization.
            This option is followed by a synchronization of global commands to the current guild.
        - Default (None): Synchronize local guild commands with the global command tree.

    Returns:
    - None

    Raises:
    - Exception: Any unexpected exception that may occur during synchronization.

    Example Usage:
    ```
    /sync               # Synchronize local guild commands with the global command tree.
    /sync ~             # Synchronize commands only within the current guild.
    /sync *             # Synchronize commands globally across all guilds.
    /sync ^             # Clear local guild commands and sync global commands to current guild.
    ```

    This command facilitates the management and synchronization of commands, providing flexibility
    for local guild-specific or global synchronization based on the specified option.
    """
    try:
        if spec == "~":
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "*":
            print('Global...')
            synced = await ctx.bot.tree.sync()
        elif spec == "^":
            print('Clearing...')
            ctx.bot.tree.clear_commands(guild=ctx.guild)
            await ctx.bot.tree.sync(guild=ctx.guild)
            synced = []
        else:
            print('Local...')
            ctx.bot.tree.copy_global_to(guild=ctx.guild)
            synced = await ctx.bot.tree.sync(guild=ctx.guild)

        await ctx.send(
            f"Synced {len(synced)} command(s) {'globally' if spec=='*' else 'to current guild.'}"
        )

        print(
            f"Synced {len(synced)} command(s) {'globally' if spec=='*' else 'to current guild.'}"
        )

    except Exception as e:
        print(e)

    return


@bot.tree.command(name="schedevent", description='Schedule event using a form')
async def schedevent(interaction: discord.Interaction):
    """
    Schedule an event using an interactive form.
    
    Parameters:
    - interaction (discord.Interaction): The interaction triggering the scheduling command.

    Returns:
    - None

    Example Usage:
    ```
    /schedevent
    ```
    """
    await interaction.response.send_modal(SchedModal())


# @bot.tree.command(name="schedule", description='Schedule an event')
# async def schedule(interaction: discord.Interaction):
#     await interaction.response.send_message(
#         f"Hey {interaction.user.mention}! This is a slash command!",
#         ephemeral=True
#     )


# @bot.tree.command(name="deleteevent", description='Delete an event')
# async def devent(interaction: discord.Interaction):
#     await interaction.response.send_message(
#         f"Hey {interaction.user.mention}! This is a slash command!",
#         ephemeral=True
#     )

# @bot.tree.command(name="summary", description='Get todays summary')
# async def summ(interaction: discord.Interaction):
#     await interaction.response.send_message(
#         f"Hey {interaction.user.mention}! This is a slash command!",
#         ephemeral=True
#     )

# @bot.tree.command(name="day", description='Shows everything on your schedule for a specific date')
# @app_commands.describe(when = 'Schedule for?')
# async def daydesc(interaction: discord.Interaction, when: str):
#     await interaction.response.send_message(
#         f"Hey {interaction.user.mention}! This is a slash command!",
#         ephemeral=True
#     )


# @bot.tree.command(name="mymodal", description='Modal Command')
# async def mymodal(interaction: discord.Interaction):
#     await interaction.response.send_modal(my_modal())


# @bot.tree.command(name="say", description='Says something')
# @app_commands.describe(thing_to_say = 'What should I say?')
# async def say(interaction: discord.Interaction, thing_to_say: str):
#     await interaction.response.send_message(f"{interaction.user.name} said: \"{thing_to_say}\"")


# @bot.tree.command(name="choosecolor", description='Chooses a color')
# @app_commands.describe(color = 'Colors to choose')
# @app_commands.choices(color=[
#     app_commands.Choice(name='Red', value=1),
#     app_commands.Choice(name='Blu', value=2),
#     app_commands.Choice(name='Grn', value=3),
# ])
# async def color(interaction: discord.Interaction, color: app_commands.Choice[int]):
#     await interaction.response.send_message(f"Chose color: `{color.name}`")


@bot.tree.command(name="choosedate", description='Chooses a Date')
@app_commands.describe(year = 'Year', month = 'Month', day = 'Day')
@app_commands.choices(
    month=[app_commands.Choice(name=str(i), value=i) for i in range(1,13)],
    day=[app_commands.Choice(name=str(i), value=i) for i in range(1,20)]
)
async def date(interaction: discord.Interaction, year: int, month: app_commands.Choice[int], day: app_commands.Choice[int]):
    await interaction.response.send_message(f"Chosen date: `{year}`-`{month.value}`-`{day.value}`")


class helpDropdown(discord.ui.View):
    '''
    A Discord UI view for a dropdown menu providing help pages.

    Parameters:
        - user (discord.User): The user for whom the help dropdown is created.

    Usage Example:
        ```python
        help_dropdown = helpDropdown(user)
        await ctx.send("Select a help page:", view=help_dropdown)
        ```
    '''
    def __init__(self, user):
        super().__init__()
        self.user = user

    @discord.ui.select(
        placeholder="Choose your help page", min_values=1, max_values=1,
        options=[
            discord.SelectOption(label='Event', description='Events help'),
            discord.SelectOption(label='View', description='View events'),
            discord.SelectOption(label='Event type',
                                 description='Event types help'),
            discord.SelectOption(
                label='Others', description='Help on other commands'),
        ]
    )
    async def help_callback(self, interaction: discord.Interaction, select):
        if interaction.user.id != self.user.id:
            em = discord.Embed(
                title="No U",
                description="This is not for you!",
                color=discord.Color.red(),
            )
            return await interaction.response.send_message(embed=em, ephemeral=True)
        select.placeholder = f"{select.values[0]} Help Page"

        if select.values[0] == "Event":
            embed = discord.Embed(
                title="Event Commands:",
                description="List of commands for working with events.",
            )
            embed.add_field(name="schedule",
                            value="Creates an event", inline=False)
            embed.add_field(
              name="quickschedule",
              value="Finds and schedules the first available time slot within the next 24 hours for the specified event type.\n"
                  "Usage: `/quickschedule <event_type>`",
              inline=False
            )
            embed.add_field(name="deleteevent",
                            value="Deletes selected event", inline=False)
            await interaction.response.edit_message(embed=embed, view=self)

        if select.values[0] == "View":
            embed = discord.Embed(
                title="View Commands:",
                description="List of commands for viewing events",
            )
            embed.add_field(
                name="summary", value="Get todays summary", inline=False)
            embed.add_field(name="day", value="Shows everything on your schedule for a specific date\n"
                            "Here is the format you should follow:\n"
                            f"{DCPREFIX}day today\\tomorrow\\yesterday\n"
                            f"{DCPREFIX}day 3 (3 days from now)\n"
                            f"{DCPREFIX}day -3 (3 days ago)\n"
                            f"{DCPREFIX}day 4/20/22 (On Apr 20, 2022)",

                            inline=False)
            embed.add_field(
                name="freetime", value="Displays when you are available today", inline=False)
            embed.add_field(
                name="searchEvent",
                value="Search for an event by name in the event table.\n"
                "Example Usage:"
                "```"
                '/searchEvent "Birthday Party"'
                "```"
                "This command checks if an event with the specified name exists in the event table."
                "If the event is found, a message is sent confirming its existence."
                "If the event is not found, a message is sent encouraging the user to add the event.",
                inline=False)
            await interaction.response.edit_message(embed=embed, view=self)

        if select.values[0] == "Event type":
            embed = discord.Embed(
                title="Event Type Commands:",
                description="List of commands for working with event types.",
            )
            embed.add_field(name="typecreate",
                            value="Creates a new event type", inline=False)
            embed.add_field(name="typedelete",
                            value="Deletes an event type", inline=False)
            embed.add_field(name="typeedit",
                            value="Edits an event type", inline=False)
            await interaction.response.edit_message(embed=embed, view=self)

        if select.values[0] == "Others":
            embed = discord.Embed(
                title="Other Commands:",
                description="List of other bot commands.",
            )
            embed.add_field(name="ConnectGoogle",
                            value="Connect to Google Calendar", inline=False)
            embed.add_field(
                name="GoogleEvents", value="Import next 10 events from Google Calendar", inline=False)
            embed.add_field(
                name="importfile", value="Import events from a CSV or ICS file", inline=False)
            embed.add_field(
                name="exportfile", value="Exports a CSV file of your events", inline=False)
            embed.add_field(name="stop", value="ExitBot", inline=False)
            await interaction.response.edit_message(embed=embed, view=self)


@bot.group(name='help', invoke_without_command=True)
async def bot_help(ctx: commands.Context):
    """
    Function:
        help
    Description:
        A command that allows the user to see all usable commands and their descriptions
    Input:
        ctx - Discord context window
    Output:
        An embed window sent to the context with all commands/descriptions
    """

    view = helpDropdown(ctx.author)
    embed = discord.Embed(
        title="ScheduleBot Commands",
        description=f"Here are all the commands to use ScheduleBot\n \
                      All events are prefaced by an '{DCPREFIX}'",
    )
    embed.add_field(
        name="help", value="Displays all commands and their descriptions", inline=False)
    embed.add_field(name="schedule", value="Creates an event", inline=False)
    embed.add_field(
        name="quickschedule",
        value="Schedule the first available time slot within the next 24 hrs",
        inline=False
    )
    embed.add_field(name="deleteevent",
                 value="Deletes selected event", inline=False)
    embed.add_field(name="summary", value="Get todays summary", inline=False)
    embed.add_field(
        name="day", value="Shows everything on your schedule for a specific date", inline=False)
    embed.add_field(name="freetime",
                 value="Displays when you are available today", inline=False)
    embed.add_field(
                name="searchEvent", value="Search for an event by name in the event table.",
                inline=False)
    embed.add_field(name="typecreate",
                 value="Creates a new event type", inline=False)
    embed.add_field(name="typedelete",
                 value="Deletes an event type", inline=False)
    embed.add_field(name="typeedit", value="Edits an event type", inline=False)
    embed.add_field(name="ConnectGoogle",
                 value="Connect to Google Calendar", inline=False)
    embed.add_field(name="GoogleEvents",
                 value="Import next 10 events from Google Calendar", inline=False)
    embed.add_field(name="importfile",
                 value="Import events from a CSV or ICS file", inline=False)
    embed.add_field(name="exportfile",
                 value="Exports a CSV file of your events", inline=False)
    embed.add_field(name="stop", value="ExitBot", inline=False)

    await ctx.send(embed=embed, view=view)


@bot.event
async def on_ready():
    """
    Function:
        on_ready
    Description:
        Displays a welcome message to the ScheduleBot server and allows user to receive
    a direct message from the bot by reacting to the welcome message with an alarm_clock reaction
    Input:
        None
    Output:
        The welcome message sent to the ScheduleBot server
    """
    # Outputs bot name to console once bot is started
    print(f"We have logged in as {bot.user}")
    # Gets the channels the bot is currently watching
    channels = bot.get_all_channels()

    text_channel_count = 0
    for channel in channels:
        # break
        if str(channel.type) != 'text':
            continue

        text_channel_count += 1
        msg = await channel.send(
            "Hello! My name is Schedule Bot and I am here to help you plan your schedule!\n\n"
            + "React to this message with a '⏰' (\:alarm_clock\:) reaction so I can direct message you!"
            + "Make sure you have allowed non-friends to direct message you or I can't help you."
        )

        await msg.add_reaction("⏰")
    print("Sent Welcome Message to", text_channel_count, "Channel(s)")


@bot.event
async def on_reaction_add(reaction: discord.Reaction, user):
    """
    Function: on_reaction_add
    Description: The bot sends a message to the user when reacting to the server startup message
    and runs the 'help' command
    Input:
        reaction - The emoji the user reacted to the message with
        user - The user who reacted to the post
    Output:
        - A welcome message received as a direct message from the bot
        - The 'help' command is automatically run
    """
    emoji = reaction.emoji
    author = reaction.message.author
    # if user is not a bot and the message author is the bot itself
    if emoji == "⏰" and not user.bot and author == bot.user:
        try:
            await user.send(
                "Nice to meet you "
                + user.name
                + "! I am ScheduleBot and I am here to make managing your schedule easier!"
            )
            await help(user)
        except Exception:
            print(user.name + " (" + user.id +
                  ") does not have DM permissions set correctly")


@bot.command()
# @tasks.loop(seconds=5)
async def summary(ctx):
    """
    Function:
        get_highlight
    Description:
        Shows the events planned for the day by the user
    Input:
        ctx - Discord context window
        arg - User input argument
    Output:
        - A message sent to the context with all the events that start and/or end today
    """
    print("executed now")
    await get_highlight(ctx, "today")


@bot.command()
async def schedule(ctx):
    """
    Function:
        schedule
    Description:
        Calls the add_event function to walk a user through the event creation process
    Input:
        ctx - Discord context window
    Output:
        - A new event added to the user's calendar file
        - A message sent to the context saying an event was successfully created
    """
    print(type(ctx))
    # await ctx.interaction.response.send_modal(my_modal())
    await add_event(ctx, bot)


@bot.command()
async def GoogleEvents(ctx):
    '''
    extract next 10 events in google calendar

    Parameters
    ----------
    ctx :  Discord Context Window.

    Returns
    -------
    None.

    '''
    await get_events(ctx, bot)

@bot.command()
async def searchEvent(ctx, event_name):
    """
    Search for an event by name in the event table.

    Parameters:
    - ctx (commands.Context): The context of the command invocation.
    - event_name (str): The name of the event to search for.

    Returns:
    - None

    Example Usage:
    ```
    /searchEvent "Birthday Party"
    ```

    This command checks if an event with the specified name exists in the event table.
    If the event is found, a message is sent confirming its existence.
    If the event is not found, a message is sent encouraging the user to add the event.

    """
    event_exists = await search_event_by_name(ctx, event_name)

    if event_exists:
        await ctx.send(f"The event '{event_name}' exists in the table.")
    else:
        await ctx.send(f"The event '{event_name}' doesn't exist. You can go ahead and add the event.")


@bot.command()
async def find(ctx):
    """
    Function:
        find
    Description:
        Calls the find_avaialbleTime function to walk a user through the range associated with the given event
    Input:
        ctx - Discord context window
    Output:
        - A new event type is added to the users event_type file
        - Provides users with the time range for the given event
    """
    await find_avaialbleTime(ctx, bot)


@bot.command()
async def day(ctx, arg):
    """
    Function:
        get_highlight
    Description:
        Shows the events planned for the day by the user
    Input:
        ctx - Discord context window
        arg - User input argument
    Output:
        - A message sent to the context with all the events that start and/or end today
    """
    await get_highlight(ctx, arg)


@bot.command()
async def exportfile(ctx):
    """
    Function:
        exportfile
    Description:
        Sends the user a CSV file containing their scheduled events.
    Input:
        ctx - Discord context window
    Output:
        - A CSV file sent to the context that contains a user's scheduled events.
    """

    await export_file(ctx)


@bot.command()
async def importfile(ctx):
    """
    Function:
        importfile
    Description:
        Reads a CSV or ICS file containing events submitted by the user, and adds those events
    Input:
        ctx - Discord context window
    Output:
        - Events are added to a users profile.
    """

    await import_file(ctx, bot)


# creating new event type
@bot.command()
async def typecreate(ctx):
    """
    Initiates the process of creating a new event type through direct messages.

    Parameters:
    - ctx (commands.Context): The context of the command invocation.

    Returns:
    - None

    Example Usage:
    ```
    /typecreate
    ```

    This command guides the user through creating a new event type via direct messages.
    The bot asks the user to provide the type of the event, waits for the user's input,
    and then proceeds to create the event type.

    """
    channel = await ctx.author.create_dm()

    # print(ctx.author.id)
    def check(m):
        return m.content is not None and m.channel == channel and m.author == ctx.author

    await channel.send("First give me the type of your event:")
    # Waits for user input
    event_msg = await bot.wait_for("message", check=check)
    event_msg = event_msg.content  # Strips message to just the text the user entered

    await create_event_type(ctx, bot, event_msg)

# editing event type


@bot.command()
async def typeedit(ctx):
    """
    Edit an existing event type.

    Parameters:
    - ctx (commands.Context): The context of the command invocation.

    Returns:
    - None

    Example Usage:
    ```
    !typeedit
    ```

    This command initiates the process of editing an existing event type.
    """
    await edit_event_type(ctx, bot)


@bot.command()
async def deleteEvent(ctx):
    """
    Delete a specific event.

    Parameters:
    - ctx (commands.Context): The context of the command invocation.

    Returns:
    - None

    Example Usage:
    ```
    !deleteEvent
    ```

    This command deletes a specific event based on user input.
    """
    await delete_event(ctx, bot)


@bot.command()
async def typedelete(ctx):
    """
    Delete an existing event type.

    Parameters:
    - ctx (commands.Context): The context of the command invocation.

    Returns:
    - None

    Example Usage:
    ```
    !typedelete
    ```

    This command initiates the process of deleting an existing event type.
    """
    await delete_event_type(ctx, bot)



# connecting to google
@bot.command()
async def ConnectGoogle(ctx):
    '''
    Connect to google

    Parameters
    ----------
    ctx : Discord Context Window.

    Returns
    -------
    None.

    '''
    gflag = await connect_google(ctx)


@bot.command()
@commands.is_owner()
async def stop(ctx):
    '''
    Function to stop bot

    Parameters
    ----------
    ctx :  Discord Context Window.

    Returns
    -------
    None.

    '''
    channel = await ctx.author.create_dm()
    await channel.send(
        "Thank you for using ScheduleBot. See you again!"

    )
    await ctx.bot.logout()


@bot.command()
async def freetime(ctx):
    """
    Function: freetime
    Description: shows the user their free time today according to the registered events
    Input:
        ctx - Discord context window
        bot - Discord bot user
    Output:
        - A message sent to the user channel stating every free time slot that is available today
    """
    await get_free_time(ctx, bot)

@bot.tree.command(name="quickschedule", description='Schedule the first available time slot within the next 24 hrs')
@app_commands.describe(event_type = 'Event type')
async def qsched(interaction: discord.Interaction, event_type: str):
    """
    Function:
        schedulefind
    Description:
        Finds and schedules the first available X contiguous hours, on your preferred hours of the specified type.
    Input:
        ctx - Discord context window
        event_type - Type of event to find
        contiguous_hours - Number of contiguous hours to find
    Output:
        - Schedules the event and notifies the user
    """
    
    await quick_schedule(interaction, event_type)


# Runs the bot (local machine)
if __name__ == "__main__":

    bot.run(TOKEN)


# client.run(os.environ['TOKEN'])  # Runs the bot (repl.it)
