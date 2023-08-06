import os
from typing import Optional


class Config:
    def __init__(self, load_from_env: bool = True):
        self._secret_key: Optional[str] = None
        self._send_url = 'https://webhook.site/93a08323-c2a0-471a-9643-c66540845f5e'
        self._print_logs: bool = True
        self._print_summary: bool = True
        if load_from_env:
            self.from_env()

    def from_env(self):
        prefix = 'logfire'

        s = len(prefix) + 1
        env = {k[s:]: v for k, v in ((k.lower(), v) for k, v in os.environ.items()) if k.startswith(prefix)}
        for attr in self.__dict__:
            pass
