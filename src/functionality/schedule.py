import discord
from discord import ui

from Event import Event
from functionality.shared_functions import add_event_to_file, get_existing_types


class SchedModal(ui.Modal, title="Schedule Event"):
    """
    A modal for scheduling events using a form.

    Components:
    - name (ui.TextInput): Text input for the event name.
    - start (ui.TextInput): Text input for the start date and time (24-hour format).
    - end (ui.TextInput): Text input for the end date and time (24-hour format).
    - priority (ui.TextInput): Text input for the event priority (1 for low, 5 for high).
    - event_type (ui.TextInput): Text input for the type of event.

    Methods:
    - on_submit: Called when the user submits the form. Sends a confirmation message.
    """
    name = ui.TextInput(
        label="Name", style=discord.TextStyle.short, placeholder="Mom's Birthday")
    start = ui.TextInput(label="Start Date + Time",
                         style=discord.TextStyle.short, placeholder="mm/dd/yy hh:mm (24hr)")
    end = ui.TextInput(label="End Date + Time",
                       style=discord.TextStyle.short, placeholder="mm/dd/yy hh:mm (24hr)")
    priority = ui.TextInput(
        label="Priority", style=discord.TextStyle.short, placeholder="1(low)-5(high)")
    event_type = ui.TextInput(
        label="Event Type", style=discord.TextStyle.short, placeholder="Party")
    # location=ui.TextInput(label="Location", style=discord.TextStyle.short, placeholder="...")
    # additional_notes=ui.TextInput(label="Additional Notes", style=discord.TextStyle.short, placeholder="...")

    async def on_submit(self, interaction: discord.Interaction):
        """
        Handle the form submission and send a confirmation message.

        Parameters:
        - interaction (discord.Interaction): The interaction associated with the form submission.

        Returns:
        - None
        """
        await interaction.response.send_message("Event Scheduled")
