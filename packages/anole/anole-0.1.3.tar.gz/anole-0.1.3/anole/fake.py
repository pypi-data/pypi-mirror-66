# -*- coding: utf-8 -*-
# @author: leesoar

import random
from threading import Lock

from anole import setting, error
from anole.tool import load_cached


class UserAgent(object):
    def __init__(self, path=setting.CACHE_PATH):
        assert isinstance(path, str), \
            'path must be string'

        self.path = path
        self.data = {}
        self.browsers = {}

        self.load()

    def load(self):
        try:
            with self.load.lock:
                self.data = load_cached(self.path)
                self.browsers = self.data['browsers']
        except error.AnoleUserAgnetError:
            setting.logger("Error occurred during fetching data, please check net status.")

    load.lock = Lock()

    def __getitem__(self, attr):
        return self.__getattr__(attr)

    def __getattr__(self, attr):
        attr = attr.lower()

        if attr == "random":
            browser = random.choice(list(self.browsers.keys()))
        else:
            browser = setting.SHORTCUTS.get(attr, attr)

        try:
            return random.choice(self.browsers[browser])
        except KeyError as e:
            raise error.AnoleUserAgnetError(f"Browser `{browser}` is not support.") from e

    def fake(self, header=None, browser="random"):
        header = header or {}

        assert isinstance(header, dict), \
            'header must be dict'

        if "user-agent" not in [key.lower() for key in header.keys()]:
            header.update({"user-agent": eval(f"self.{browser}")})

        return header

