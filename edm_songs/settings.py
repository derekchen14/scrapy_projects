# -*- coding: utf-8 -*-

# Scrapy settings for edm_songs project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'edm_songs'

SPIDER_MODULES = ['edm_songs.spiders']
NEWSPIDER_MODULE = 'edm_songs.spiders'
USER_AGENT = "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36"

# Crawl responsibly by identifying yourself (and your website) on the user-agent
