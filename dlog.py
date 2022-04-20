"""discord-logger"""

import logging
from discord import Webhook, RequestsWebhookAdapter


class DiscordHandler(logging.Handler):
    """
    A handler class which logs to discord with the provided 
    webhook URL
    """

    def __init__(
            self,
            webhook_url: str
    ):
        super(DiscordHandler, self).__init__()

        self.webhook_url = webhook_url
        self.webhook = Webhook.from_url(
            self.webhook_url,
            adapter=RequestsWebhookAdapter()
        )

    def emit(self, record):
        """Sends message to Discord"""
        try:
            msg = self.format(record)
            print(msg)
            self.webhook.send(content=msg)
            self.flush()
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception:
            self.handleError(record)
