# -*- coding: utf-8 -*-
# @author: leesoar

"""tools"""

import json
import os

import requests
from retrying import retry

from anole import setting


@retry(stop_max_attempt_number=setting.HTTP_RETRY)
def get(url):
    res = requests.get(url)
    return res


def update(path, data):
    os.path.exists(path) and os.remove(path)
    open(path, encoding="utf-8", mode="w").write(data)


def read(path):
    return json.loads(open(path, encoding="utf-8").read())


def load_cached(path):
    if not os.path.exists(path):
        update(path, get(setting.CACHE_URL).text)
    return read(path)

