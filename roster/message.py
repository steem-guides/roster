# -*- coding:utf-8 -*-

import traceback

from utils.logging.logger import logger


def get_message(id, footer=False):
    return build_message(id, footer)

def build_message(id, footer=False, message_marker=False):
    message = MESSAGES[id]

    if footer and id in FOOTERS:
        message += FOOTERS[id]
    if message_marker:
        message += MESSAGE_ID.format(message_id=id)

    return message

MESSAGE_ID = """
<div message_id=\"{message_id}\"></div>
"""

MESSAGES = {}
FOOTERS = {}

MESSAGES["roste"] = """

"""
