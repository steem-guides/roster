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


TABLE_TEMPLATE = """
<table>
<thead>
<tr>
{head}
</tr>
</thead>
<tbody>
{body}
</tbody>
</table>
"""

def build_table(head, data):
    if head and data and len(head) > 0 and len(data) > 0:
        head = "\n".join(["  <th>{}</th>".format(c) for c in head])
        rows = []
        for row in data:
            row_md = "\n".join(["<tr>", "\n".join(["  <td>{}</td>".format(c) for c in row]), "</tr>"])
            rows.append(row_md)
        body = "\n".join(rows)
        table = TABLE_TEMPLATE.format(head=head, body=body)
        return table
    return ""


MESSAGE_ID = """
<div message_id=\"{message_id}\"></div>
"""

MESSAGES = {}
FOOTERS = {}

MESSAGES["roster"] = """
本页面为 **Steem 花名册**，由 [@steem-guides](https://busy.org/@steem-guides) 创建。

其目的在于帮助社区成员（尤其是新人），更方便地记忆他人的别名。

页面根据 Steem 社区中的文章描述和对话自动生成。目前生成花名册参考的主要数据源有：
{sources}

- - -

现在已知的花名册的名单如下：
{table}
"""
