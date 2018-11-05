"""Handles messages to discord."""
from discord_webhook import DiscordWebhook, DiscordEmbed
import local_env


class Discord():
    """Handles messages to discord.

    This requires you to create your own Discord server in order to recieve
    messages from the script. You can read more about webhooks here:
    https://support.discordapp.com/hc/en-us/articles/228383668-Intro-to-Webhooks

    Add your webhooks to the local_env.py file.
    """

    INFO = 0
    ERROR = 1

    @classmethod
    def send_message(self, text, level):
        """Send message to webhook."""
        if level == 0:  # info
            title = "INFO"
            color = 242424
            url = local_env.INFO_URL
        elif level == 1:  # exception
            title = "ERROR"
            color = 16711680
            url = local_env.ERROR_URL

        webhook = DiscordWebhook(url=url)
        embed = DiscordEmbed(title=title, description=text, color=color)
        embed.set_timestamp()
        webhook.add_embed(embed)
        webhook.execute()
        return
