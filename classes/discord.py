"""Handles messages to discord."""
from discord_webhook import DiscordWebhook, DiscordEmbed
import usersettings as userset


class Discord:
    """Handles messages to discord.

    This requires you to create your own Discord server in order to recieve
    messages from the script. You can read more about webhooks here:
    https://support.discordapp.com/hc/en-us/articles/228383668-Intro-to-Webhooks

    Add your webhooks to the usersettings.py file.
    """

    INFO = 0
    ERROR = 1

    @staticmethod
    def send_message(text :str, level :int =INFO) -> None:
        """Send message to webhook.
        
        Keyword arguments
        text  -- Text of the message to send to the Discord webhook.
        level -- Whether to send an info message or error message.
        """
        url = ""
        if level == Discord.INFO:
            title = "INFO"
            color = 242424
            url = userset.INFO_URL

        elif level == Discord.ERROR:
            title = "ERROR"
            color = 16711680
            url = userset.ERROR_URL
            if not url: url = userset.INFO_URL

        if not url:
            return

        webhook = DiscordWebhook(url=url)
        embed = DiscordEmbed(title=title, description=text, color=color)
        embed.set_timestamp()
        webhook.add_embed(embed)
        webhook.execute()
        return
