"""discord-logger"""

import typing
import logging
import discord
import datetime


class DiscordHandler(logging.Handler):
    """
    A handler class which logs to discord with the provided
    webhook URL
    
    Warning: Don't set the logging level to debug, otherwise
    there wil be recursion.
    """

    def __init__(
            self,
            webhook_url: str
    ) -> None:
        super(DiscordHandler, self).__init__()

        self.webhook_url = webhook_url
        self.webhook = discord.Webhook.from_url(
            self.webhook_url,
            adapter=discord.RequestsWebhookAdapter()
        )

    def _make_embed(
            self,
            record: logging.LogRecord
    ) -> typing.Tuple[discord.Embed, str]:
        """
        Change these settings to customise

        Returns a tuple of the embed and the message str
        """
        colour_mapping = {
            "NOTSET": discord.Colour.darker_grey(),
            "DEBUG": discord.Colour.dark_gray(),
            "INFO": discord.Colour.blue(),
            "WARNING": discord.Colour.gold(),
            "ERROR": discord.Colour.orange(),
            "CRITICAL": discord.Colour.red()
        }
        included_fields = {
            "created": False,
            "filename": True,
            "funcName": True,
            "levelname": False,
            "levelno": False,
            "message": False,
            "module": True,
            "msecs": False,
            "name": False,
            "pathname": False,
            "process": True,
            "processName": True,
            "relativeCreated": False,
            "thread": True,
            "threadName": False
        }
        field_names = {
            "created": "Log time",
            "filename": "Filename",
            "funcName": "Function name",
            "levelname": "Level name",
            "levelno": "Level number",
            "message": "Message",
            "module": "Module name",
            "msecs": "Milliseconds",
            "name": "Logger name",
            "pathname": "Full path",
            "process": "Process ID",
            "processName": "Process name",
            "relativeCreated": "Time delta",
            "thread": "Thread ID",
            "threadName": "Thread name"
        }
        embed = discord.Embed(
            title=record.levelname,
            description=self.format(record),
            timestamp=datetime.datetime.now(),
            color=colour_mapping.pop(record.levelname, discord.Colour.darker_grey()),

        )

        # Add fields
        for field_name in included_fields:
            if included_fields[field_name]:
                field_value = getattr(record, field_name)
                new_field_name = field_names[field_name]
                embed.add_field(name=new_field_name, value=field_value, inline=True)

        embed.set_footer(text="This message was automatically generated.")
        current_datetime = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S:%f')
        message = f"Logging event at {current_datetime[:-2]}"

        return embed, message

    def emit(
            self,
            record: logging.LogRecord
    ) -> None:
        """Sends message to Discord"""
        try:
            embed, message = self._make_embed(record)
            self.webhook.send(
                embed=embed,
                content=message
            )
            self.flush()
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception:
            self.handleError(record)
