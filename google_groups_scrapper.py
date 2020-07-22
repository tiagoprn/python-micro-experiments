#coding: utf-8
# based on code from: https://sputnikus.github.io/google_groups_scrape
import os
import time
from lxml.html import fromstring  # ,date_parse
from selenium import webdriver
from selenium.webdriver.common.proxy import *


def thread_to_dict(thread):
    parsed = {'name': thread.xpath('.//a[@class="GIEUOX-DPL"]')[0].text}
    parsed['url'] = thread.xpath('.//a[@class="GIEUOX-DPL"]')[0].attrib['href']
    raw_last_change = thread.xpath('.//span[@class="GIEUOX-DOQ"]/span')[0].attrib['title']
    # last_change = date_parse(raw_last_change)
    parsed['month'] = last_change.month
    info = thread.xpath('.//span[@class="GIEUOX-DOQ"]')
    parsed['seen'] = int(info[1].text.split()[0])
    parsed['posts'] = int(info[0].text.split()[0])
    return parsed

GOOGLE_GROUP_BASE = 'https://groups.google.com/forum/'
# GOOGLE_GROUP_URL = GOOGLE_GROUP_BASE + '#!forum/{}'
GOOGLE_GROUP_URL = GOOGLE_GROUP_BASE + '#!forum/{}/?hl=en'
GROUP_URL = GOOGLE_GROUP_URL.format('nsndev')

proxy = os.environ.get('http_proxy')
if proxy:
    PROXY_HOST, PROXY_PORT = os.environ.get('http_proxy').split('//')[1].split(':')
    PROXY_PORT = int(PROXY_PORT)

    fp = webdriver.FirefoxProfile()
    fp.set_preference("network.proxy.type", 1)
    fp.set_preference("network.proxy.http", PROXY_HOST)
    fp.set_preference("network.proxy.http_port", PROXY_PORT)
    fp.set_preference("network.proxy.ftp", PROXY_HOST)
    fp.set_preference("network.proxy.ftp_port", PROXY_PORT)
    fp.set_preference("network.proxy.ssl", PROXY_HOST)
    fp.set_preference("network.proxy.ssl_port", PROXY_PORT)
    # fp.set_preference("general.useragent.override", "whater_useragent")
    fp.update_preferences()

    browser = webdriver.Firefox(firefox_profile=fp)
else:
    browser = webdriver.Firefox()

browser.implicitly_wait(30)
# browser.set_window_size(1024, 768)
browser.get(GROUP_URL)
frontpage = fromstring(browser.page_source)
browser.quit()
frontpage.make_links_absolute(GOOGLE_GROUP_BASE)
html_threads = frontpage.xpath('//div[@class="GIEUOX-DEQ"]')
threads = (thread_to_dict(thread) for thread in html_threads)
