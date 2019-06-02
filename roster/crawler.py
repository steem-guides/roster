# -*- coding:utf-8 -*-

import os
import re
import pandas as pd

from steem.collector import get_comments
from steem.comment import SteemComment
from steem.settings import settings, STEEM_HOST
from data.reader import SteemReader
from roster.message import build_message, build_table
from utils.logging.logger import logger
from utils.csv.csv_writer import write_json_array_to_csv


TEAMCN_SHOP_POST_NAME_NICKNAME_PATTERN = r"\|(\@[A-Za-z0-9._-]+) ([^|]+)\|"
TEAMCN_SHOP_COMMENT_NAME_NICKNAME_PATTERN = r"^你好鸭，([^!]+)!"

SOURCES = """
1. @teamcn-shop 新手村小卖部日报: https://steemit.com/@teamcn-shop
1. @teamcn-shop 新手村小卖部 送外卖给客户时的留言。例如 [这条留言](https://busy.org/@julian2013/p109-6kbf9ubevi#@teamcn-shop/annepink-re-julian2013-p109-6kbf9ubevi-20190602t133509529z)
"""

SAVED_ROSTER_DATA = "https://raw.githubusercontent.com/steem-guides/roster/gh-pages/roster.csv"
NICKNAME_DELIMITER = " / "


class RosterCrawler(SteemReader):

    def __init__(self, account=None, tag=None, days=None, incremental=False):
        SteemReader.__init__(self, account=account, tag=tag, days=days)
        self.roster = []
        self._roster_dict = {}
        self.public_folder = "public"
        self.incremental = incremental
        if self.incremental:
            logger.info("launch: incremental mode")
            self.days = 1.5
            self.fetch_history()

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

    def get_latest_comments(self):
        return get_comments(account=self.account, days=self.days, limit=self.limit)

    def crawl(self):
        if len(self.posts) == 0:
            self.get_latest_posts()

        # crawl posts
        if len(self.posts) > 0:
            for post in self.posts:
                self.parse_post(post)
        else:
            logger.info("No posts are fetched.")

        # crawl comments
        comments = self.get_latest_comments()
        if len(comments) > 0:
            for c in comments:
                self.parse_comment(c)
        else:
            logger.info("No comments are fetched")

    def _update(self, account, name):
        if not account in self._roster_dict:
            self._roster_dict[account] = [name]
            return True
        else:
            if not name in self._roster_dict[account]:
                self._roster_dict[account].append(name)
                return True
        return False

    def parse_post(self, post):
        res = re.findall(TEAMCN_SHOP_POST_NAME_NICKNAME_PATTERN, post.body)
        if res:
            for r in res:
                account = r[0]
                nickname = r[1]
                self._update(account, nickname)

    def parse_comment(self, comment):
        res = re.search(TEAMCN_SHOP_COMMENT_NAME_NICKNAME_PATTERN, comment.body)
        if res:
            parent_account = comment["parent_author"]
            nickname = res.group(1)
            if parent_account != nickname:
                account = "@" + parent_account
                self._update(account, nickname)

    def build(self):
        self.transform()
        count = len(self.roster)
        if count > 0:
            self.save()
            self.publish()
        return count

    def transform(self):
        if len(self._roster_dict) > 0:
            self.roster = [{"account": k, "nickname": NICKNAME_DELIMITER.join(v)} for (k, v) in sorted(self._roster_dict.items())]

    def save(self):
        count = len(self.roster)
        if count > 0:
            filename = self._get_roster_data_file()
            write_json_array_to_csv(self.roster, filename)
            logger.info("Crawled {} names to add into roster {}".format(count, filename))

    def fetch_history(self):
        try:
            df = pd.read_csv(SAVED_ROSTER_DATA)
            self.roster = df.to_dict('records')
            for item in self.roster:
                self._roster_dict[item['account']] = item['nickname'].split(NICKNAME_DELIMITER)
            logger.info("Roster history has been fetched from the server. {} users are found.".format(len(self.roster)))
        except:
            logger.info("Failed to fetch roster history from server")

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

