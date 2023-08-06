# -*- coding: utf-8 -*-
# @author: leesoar

"""settings"""

import logging
import os
import tempfile

__version__ = "0.1.0"

logger = logging.getLogger(__package__)

CACHE_PATH = os.path.join(tempfile.gettempdir(), f"anole_{__version__}.json")

CACHE_URL = f"https://www.leesoar.com/file/anole_{__version__}.json"

SHORTCUTS = {
    'internet explorer': 'internetexplorer',
    'ie': 'internetexplorer',
    'msie': 'internetexplorer',
    'edge': 'internetexplorer',
    'gg': 'chrome',
    'google': 'chrome',
    'googlechrome': 'chrome',
    'ff': 'firefox',
}

HTTP_RETRY = 5
