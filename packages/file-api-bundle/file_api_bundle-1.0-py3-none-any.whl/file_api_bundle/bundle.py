from applauncher.kernel import ConfigurationReadyEvent
from file_api import Client

import logging


class FileApiBundle(object):
    def __init__(self):
        self.logger = logging.getLogger("file_api_bundle")
        self.config_mapping = {
            "file_api": {
                "token": None,
                "default_namespace": "",
            }
        }

        self.event_listeners = [
            (ConfigurationReadyEvent, self.config_ready),
        ]

        self.injection_bindings = {}

    def config_ready(self, event):
        config = event.configuration.file_api
        self.injection_bindings[Client] = Client(
            default_namespace=config.default_namespace if config.default_namespace else None,
            token=config.token
        )
