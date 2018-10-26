#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
import os
import sys
import time
import math
import urllib2
import urlparse
import optparse
from cgi import escape
import traceback
from Queue import Queue, Empty as QueueEmpty
from bs4 import BeautifulSoup


__version__ = "0.1"
__copyright__ = "CopyRight (C) 2018 by Jinmiao Li"
__license__ = "MIT"
__author__ = "Jinmiao Li <beikejinmiao@gmail.com>"

USAGE = "%prog [options] <url>"
VERSION = "%prog v" + __version__

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100"
down_home = "/data2/pcap/download"


class Crawler(object):

    def __init__(self):
        self.root = None
        self.urls = []
        self.queue = Queue()
        self.args = self._parse_args()
        self.host = urlparse.urlparse(self.root)[1]

    def _init_args(self):
        """parse_options() -> opts, args

        Parse any command-line options given returning both
        the parsed options and arguments.
        """

        parser = optparse.OptionParser(usage=USAGE, version=VERSION)

        parser.add_option("-q", "--quiet",
                          action="store_true", default=False, dest="quiet",
                          help="Enable quiet mode")

        parser.add_option("-l", "--links",
                          action="store_true", default=False, dest="links",
                          help="Get links for specified url only")

        parser.add_option("-d", "--depth",
                          action="store", type="int", default=30, dest="depth",
                          help="Maximum depth to traverse")

        parser.add_option("-o", "--output", dest="output",
                          help="The output file path of the urls that has crawled")

        parser.add_option("--input-ignore", dest="input_ignore",
                          help="The input file path of the urls that need to ignore")

        parser.add_option("--ignore-param",
                          action="store_true", default=True,  dest="ignore_param",
                          help="Ignore parameter in url while traversing")

        parser.add_option("--same-origin",
                          action="store_true", default=True, dest="same_origin",
                          help="Only crawl the url with the same host as root page")

        return parser.parse_args()

    def _parse_args(self):
        opts, args = self._init_args()
        if len(args) < 1:
            print(USAGE)
            sys.exit(1)

        self.root = args[0]
        self.queue.put(self.root)
        self.urls.append(self.root)
        return opts

    def crawl(self, depth):
        # if depth > self.args.depth:
        #     return
        # try:
        #     url = self.queue.get()
        # except QueueEmpty:
        #     return
        #
        # self.fetch(url)
        # self.crawl(depth+1)
        while True:
            try:
                url = self.queue.get(block=True, timeout=1)
            except QueueEmpty:
                break
            self.fetch(url)

    @staticmethod
    def _add_headers(request):
        request.add_header("User-Agent", USER_AGENT)

    @staticmethod
    def open(url):
        request = urllib2.Request(url)
        handle = urllib2.build_opener()
        return request, handle

    def _url_filter(self, url):
        if self.args.ignore_param:
            url = re.sub("\?.*", "", url)

        host = urlparse.urlparse(url)[1]
        if self.args.same_origin and not re.match(".*%s" % self.host, host):
            return None
        if url in self.urls:
            return None

        return url

    def _response(self, url):
        content = None
        request, handle = self.open(url)
        if request and handle:
            self._add_headers(request)
            full_url = request.get_full_url()
            # save to file
            if "." in os.path.basename(full_url):
                if full_url.endswith(".pcap") or full_url.endswith(".zip"):
                    site = handle.open(request)
                    meta = site.info()
                    content_length = meta.getheaders("Content-Length")
                    if len(content_length) >= 1:
                        if int(content_length[0]) < 50000000:   # 50M
                            content = site.read()
                            save2file(content, full_url)
                            print("Save: %s" % full_url)
                        else:
                            print("Found big file: %s, size: %s, type: %s" % (
                                full_url, content_length[0], meta.getheader("Content-Type")))
                return None
            else:
                content = handle.open(request).read()

        return content

    def fetch(self, parent):
        urls = list()
        link_tags = []

        try:
            content = self._response(parent)
            # extract html
            if content:
                soup = BeautifulSoup(content, features="lxml")
                link_tags = soup('a')
        except urllib2.HTTPError as error:
            if error.code == 404:
                print("ERROR: %s -> %s" % (error, error.url))
            else:
                print("ERROR: %s" % error)
        except:
            print("ERROR: %s" % parent)
            print(traceback.format_exc())

        for tag in link_tags:
            href = tag.get("href")
            if href is None:
                continue

            url = urlparse.urljoin(parent, escape(href))
            url = self._url_filter(url)
            if url:
                urls.append(url)
                self.queue.put(url)
                self.urls.append(url)

        return urls

    def show_links(self):
        urls = self.fetch(self.root)
        for i, url in enumerate(urls):
            print("%d. %s" % (i, url))


def save2file(content, url):
    url_items = url.split("/")
    filename = url_items[-1]
    dirpath = os.path.join(down_home, "/".join(url_items[3:-1]))
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)
    with open(os.path.join(dirpath, filename), "wb+") as fopen:
        fopen.write(content)


def main():
    crawler = Crawler()
    if crawler.args.links:
        crawler.show_links()
        sys.exit(0)

    print("Crawling '%s' (Max Depth: %d)" % (crawler.root, crawler.args.depth))
    crawler.crawl(0)
    # print("\n".join(crawler.urls))


if __name__ == "__main__":
    main()

