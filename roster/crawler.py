# -*- coding:utf-8 -*-

import os
import re

from steem.comment import SteemComment
from steem.settings import settings, STEEM_HOST
from data.reader import SteemReader
from roster.message import build_message, build_table
from utils.logging.logger import logger
from utils.csv.csv_writer import write_json_array_to_csv


NAME_NICKNAME_PATTERN = r"\|(\@[A-Za-z0-9._-]+) ([^|]+)\|"

SOURCES = """
1. @teamcn-shop 新手村小卖部日报: https://steemit.com/@teamcn-shop
"""


class RosterCrawler(SteemReader):

    def __init__(self, account=None, tag=None, days=None, incremental=False):
        SteemReader.__init__(self, account=account, tag=tag, days=days)
        self.roster = []
        self._roster_dict = {}
        self.public_folder = "public"
        self.incremental = incremental
        if self.incremental:
            self.days = 1.5

    def get_name(self):
        name = "roster"
        target = self.account or self.tag
        return "{}-{}-{}".format(name, target, self._get_time_str())

    def _check_folder_existence(self):
        if not os.path.exists(self.public_folder):
            os.makedirs(self.public_folder)

    def _get_roster_data_file(self):
        filename = os.path.join(self.public_folder, "roster.csv")
        self._check_folder_existence()
        return filename

    def _get_roster_page_file(self):
        filename = os.path.join(self.public_folder, "index.md")
        self._check_folder_existence()
        return filename

    def is_qualified(self, post):
        return True

    def crawl(self):
        if len(self.posts) == 0:
            self.get_latest_posts()

        count = 0
        if len(self.posts) > 0:
            for post in self.posts:
                names = self.parse(post)
            self.transform()
            count = len(self.roster)
            if count > 0:
                self.save()
                self.publish()

        else:
            logger.info("No new posts are fetched.")
        return len(self.roster)

    def _update(self, account, name):
        if not account in self._roster_dict:
            self._roster_dict[account] = [name]
            return True
        else:
            if not name in self._roster_dict[account]:
                self._roster_dict[account].append(name)
                return True
        return False

    def parse(self, post):
        c = SteemComment(comment=post)
        res = re.findall(NAME_NICKNAME_PATTERN, c.get_comment().body)

        names = []
        if res:
            for r in res:
                account = r[0]
                nickname = r[1]
                self._update(account, nickname)
        return names

    def transform(self):
        if len(self._roster_dict) > 0:
            self.roster = [{"account": k, "nickname": " / ".join(v)} for (k, v) in sorted(self._roster_dict.items())]

    def save(self):
        count = len(self.roster)
        if count > 0:
            filename = self._get_roster_data_file()
            write_json_array_to_csv(self.roster, filename)
            logger.info("Crawled {} names to add into roster {}".format(count, filename))

    def prefetch(self):
        pass

    def _sources(self):
        return SOURCES

    def _get_account_link(self, name):
        return "https://busy.org/{}".format(name)

    def _content(self):
        if len(self.roster) > 0:
            names = [("<a href=\"{}\">{}</a>".format(self._get_account_link(user['account']), user['account']),
                      user['nickname']
                      ) for user in self.roster]
            table = build_table(("用户", "别名"), names)
            template = build_message("roster")
            return template.format(sources=self._sources(), table=table)
        else:
            return None

    def publish(self):
        count = len(self.roster)
        if count > 0:
            filename = self._get_roster_page_file()
            content = self._content()
            with open(filename, "w", encoding="utf-8") as f:
                f.write(content)
            logger.info("Publish {} names into the page {}".format(count, filename))

