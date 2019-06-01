# -*- coding:utf-8 -*-

import os
import re

from steem.comment import SteemComment
from steem.settings import settings, STEEM_HOST
from data.reader import SteemReader
from utils.logging.logger import logger
from utils.csv.csv_writer import write_json_array_to_csv


NAME_NICKNAME_PATTERN = r"\|(\@[A-Za-z0-9._-]+) ([^|]+)\|"


class RosterCrawler(SteemReader):

    def __init__(self, account=None, tag=None, days=None, incremental=False):
        SteemReader.__init__(self, account=account, tag=tag, days=days)
        self.roster = []
        self.incremental = incremental
        if self.incremental:
            self.days = 1.5

    def get_name(self):
        name = "roster"
        target = self.account or self.tag
        return "{}-{}-{}".format(name, target, self._get_time_str())

    def _get_roster_file(self):
        folder = "public"
        filename = os.path.join(folder, "roster.csv")
        if not os.path.exists(folder):
            os.makedirs(folder)
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
                self.roster.extend(names)
            count = len(self.roster)
            if count > 0:
                self.save()
            logger.info("Crawled {} names to add into roster {}".format(count, self._get_roster_file()))
        else:
            logger.info("No new posts are fetched.")
        return len(self.roster)

    def parse(self, post):
        c = SteemComment(comment=post)
        res = re.findall(NAME_NICKNAME_PATTERN, c.get_comment().body)

        known_names = [user['account'] for user in self.roster]

        names = []
        if res:
            for r in res:
                name = {
                    "account": r[0],
                    "nickname": r[1]
                }
                if not name['account'] in known_names:
                    names.append(name)
        return names

    def save(self):
        write_json_array_to_csv(self.roster, self._get_roster_file())

    def fetch(self):
        pass

    def publish(self):
        pass

