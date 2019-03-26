"""Handles messages to discord."""
from discord_webhook import DiscordWebhook, DiscordEmbed
import usersettings as userset


class Discord():
    """Handles messages to discord.

    This requires you to create your own Discord server in order to recieve
    messages from the script. You can read more about webhooks here:
    https://support.discordapp.com/hc/en-us/articles/228383668-Intro-to-Webhooks

    Add your webhooks to the usersettings.py file.
    """

    INFO = 0
    ERROR = 1

    @classmethod
    def send_message(self, text, level):
        """Send message to webhook."""
        url = ""
        if level == 0:  # info
            title = "INFO"
            color = 242424
            url = userset.INFO_URL
        elif level == 1:  # exception
            title = "ERROR"
            color = 16711680
            url = userset.ERROR_URL

        if not url:
            return

        webhook = DiscordWebhook(url=url)
        embed = DiscordEmbed(title=title, description=text, color=color)
        embed.set_timestamp()
        webhook.add_embed(embed)
        webhook.execute()
        return
