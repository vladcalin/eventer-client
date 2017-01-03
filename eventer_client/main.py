import socket
import random
import time

import requests

from eventer_client.exceptions import ServerError


class Event(object):
    def __init__(self, category, url, source=None):
        self._category_id = category
        self._service_url = url
        self._values = {}
        if not source:
            self._source = self.autodiscover_source()

    def __setattr__(self, key, value):
        if key.startswith("_") and key not in ("from_dict", "submit", "autodiscover_source"):
            return super(Event, self).__setattr__(key, value)
        self._values[key] = value

    @classmethod
    def from_dict(cls, category, url, values, source=None):
        instance = cls(category, url, source)
        for k, v in values.items():
            setattr(instance, k, v)
        return instance

    def submit(self):
        resp = requests.post(self._service_url,
                             json={
                                 "jsonrpc": "2.0",
                                 "method": "submit_event",
                                 "params": {
                                     "source": self._source,
                                     "category": self._category_id,
                                     "values": self._values
                                 },
                                 "id": 1
                             })
        resp_dict = resp.json()
        if resp_dict["error"]:
            raise ServerError(resp_dict["error"])

    @staticmethod
    def autodiscover_source():
        return socket.getfqdn()


if __name__ == '__main__':
    event = Event(category="585a34dfa3b2ac2a641e6eb6", url="http://localhost/api")

    event.filename = "hello_world.exe"
    event.extension = "exe"
    event.size = 1099910
    event.is_malware = False
    event.submit()

    words = ["hello", "world", "how", "you", "doing", "prize", "free", "malware", "antivirus", "Error", "friend",
             "dolphin"]
    extensions = ["exe", "bat", "rar", "zip", "pdf", "txt", "py", "tar.gz", "iso"]
    while True:
        ext = random.choice(extensions)
        Event.from_dict("585a34dfa3b2ac2a641e6eb6",
                        "http://localhost/api",
                        {
                            "filename": random.choice(words) + "_" + random.choice(words) + "." + ext,
                            "extension": ext,
                            "size": random.randint(10000, 20000),
                            "is_malware": random.choice([True, False])
                        }).submit()
        time.sleep(random.randint(0, 5))
