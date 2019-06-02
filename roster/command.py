# -*- coding:utf-8 -*-

import os, time, random
from invoke import task

from utils.logging.logger import logger
from steem.settings import settings
from roster.crawler import RosterCrawler


@task(help={
      'account': 'the account of the blogs to download',
      'tag': 'the tag of the blogs to download',
      'days': 'the posts in recent days to fetch',
      'debug': 'enable the debug mode',
      'production': 'set production mode to download incrementally'
      })
def generate(ctx, account="teamcn-shop", tag=None, days=None, debug=False, production=False):
    """ generate the roster from the specified sources """

    if debug:
        settings.set_debug_mode()

    settings.set_steem_node()

    account = account or settings.get_env_var("STEEM_ACCOUNT")
    tag = tag or settings.get_env_var("STEEM_TAG")
    days = days or settings.get_env_var("DURATION")
    incremental = settings.get_env_var("INCREMENTAL") or False

    crawler = RosterCrawler(account=account, tag=tag, days=days, incremental=incremental)
    crawler.crawl()
    return crawler.build()
