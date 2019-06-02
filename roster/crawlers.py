# -*- coding:utf-8 -*-

import os
import re

from steem.comment import SteemComment
from steem.collector import get_posts, get_comments
from utils.logging.logger import logger


TEAMCN_SHOP_ACCOUNT = "teamcn-shop"

TEAMCN_SHOP_POST_NAME_NICKNAME_PATTERN = r"\|(\@[A-Za-z0-9._-]+) ([^|]+)\|"
TEAMCN_SHOP_COMMENT_NAME_NICKNAME_PATTERN = r"^你好鸭，([^!]+)!"

TEAMCN_CEREMONY_POST = "https://steemit.com/@team-cn/egxwc0ewsi"
TEAMCN_CEREMONY_NAME_NICKNAME_PATTERN = r"\n(\@[A-Za-z0-9._-]+)\s+(\S+)"


class Crawler:

    def __init__(self, roster_dict):
        self._roster_dict = roster_dict or {}

    def _update(self, account, name):
        if not account in self._roster_dict:
            self._roster_dict[account] = [name]
            return True
        else:
            if not name in self._roster_dict[account]:
                self._roster_dict[account].append(name)
                return True
        return False

    def run(self):
        # crawl posts
        posts = self.crawl()
        if len(posts) > 0:
            for post in posts:
                self.parse(post)
        else:
            logger.info("No posts are fetched.")

        return self._roster_dict


class TeamCnShopDaily(Crawler):

    def __init__(self, roster_dict, days):
        Crawler.__init__(self, roster_dict)
        self.account = TEAMCN_SHOP_ACCOUNT
        self.days = days
        logger.info("Crawling roster from teamcn-shop daily posts...")

    def crawl(self):
        return get_posts(account=self.account, days=self.days)

    def parse(self, post):
        res = re.findall(TEAMCN_SHOP_POST_NAME_NICKNAME_PATTERN, post.body)
        if res:
            for r in res:
                account = r[0]
                nickname = r[1]
                self._update(account, nickname)


class TeamCnShopComments(Crawler):

    def __init__(self, roster_dict, days):
        Crawler.__init__(self, roster_dict)
        self.account = TEAMCN_SHOP_ACCOUNT
        self.days = days
        logger.info("Crawling roster from teamcn-shop comments...")

    def crawl(self):
        return get_comments(account=self.account, days=self.days)

    def parse(self, comment):
        res = re.search(TEAMCN_SHOP_COMMENT_NAME_NICKNAME_PATTERN, comment.body)
        if res:
            parent_account = comment["parent_author"]
            nickname = res.group(1)
            if parent_account != nickname:
                account = "@" + parent_account
                self._update(account, nickname)

class TeamCnCeremony(Crawler):

    def __init__(self, roster_dict):
        Crawler.__init__(self, roster_dict)
        logger.info("Crawling roster from teamcn ceremony posts...")

    def crawl(self):
        post = SteemComment(url=TEAMCN_CEREMONY_POST).get_comment()
        return [post]

    def parse(self, post):
        name_list_section = post.body.split("新手村村民名单")[-1]
        res = re.findall(TEAMCN_CEREMONY_NAME_NICKNAME_PATTERN, name_list_section)
        if res:
            for r in res:
                account = r[0]
                nicknames = r[1]
                for nickname in nicknames.split("/"):
                    if nickname != "TBD":
                        self._update(account, nickname)




