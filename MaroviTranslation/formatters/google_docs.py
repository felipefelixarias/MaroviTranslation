import os

from MaroviTranslation.clients.google_docs import GoogleDocClient

from .core import Formatter

class GoogleDocFormatter(Formatter):
    def __init__(self, config):
        super(GoogleDocFormatter, self).__init__(config)
        self.client = GoogleDocClient(config)

    def format(self, translation):
        self.client.update_document(translation)

        