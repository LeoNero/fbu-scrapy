# -*- coding: utf-8 -*-

BOT_NAME = 'news'

SPIDER_MODULES = ['news.spiders']
NEWSPIDER_MODULE = 'news.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure item pipelines
# Parse settings
PARSE_APP_ID = 'LeoHaleyPlaxides'
PARSE_MASTER_KEY = 'LeoHaleyPlaxides'
PARSE_SERVER_URL = 'http://fbu-team-app.herokuapp.com/parse'
