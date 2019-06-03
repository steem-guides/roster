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

花名册的目的在于帮助社区成员（尤其是新人），更好地记忆社区里朋友们的别名。

- - -

现在已知的花名册的名单如下，包含 **{count}** 名社区成员：
{table}

- - -

要了解他们的故事和过往，建议阅读：

- [《Steem指北》](https://steem-guides.github.io/steemh/fl.html)
- [新手村访谈](https://steemblog.github.io/@team-cn/tags/cn-interview/)


本名册根据 Steem 社区中的文章和对话自动生成。目前参考的数据源包括：
{sources}

如有任何建议，欢迎联系：[@steem-guides](https://busy.org/@steem-guides) 或 [@robertyan](https://busy.org/@robertyan)

"""
