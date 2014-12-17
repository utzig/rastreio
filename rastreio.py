#!/usr/bin/env python

from os.path import expanduser
from HTMLParser import HTMLParser
import urllib2
import re

"""
This class is used to parse the table data received back by the
online lookup for each tracking code
"""
class TableParser(HTMLParser):
    def __init__(self):
        HTMLParser.reset(self)
        self.accept = False
        self.table_data = []

    def handle_starttag(self, tag, attrs):
        if self.accept:
            self.table_data.append(tag)
        if tag == 'table':
            self.accept = True

    def handle_endtag(self, tag):
        if self.accept:
            self.table_data.append(tag)
        if tag == 'table':
            self.accept = False

    def handle_data(self, data):
        if self.accept:
            self.table_data.append(data)

"""
Receives the tracking code as string and does online search.
Returns the html received from the page lookup
"""
def lookup(tracking_code):
    params = 'Z_ACTION=Search&P_TIPO=001&P_LINGUA=001&P_COD_UNI=' + tracking_code
    url = "http://websro.correios.com.br/sro_bin/txect01$.QueryList"
    req = urllib2.Request(url, params)
    return urllib2.urlopen(req).read()

def pretty_print(html_data):
    parser = TableParser()
    parser.feed(html_data)
    for table in parser.table_data: print table

config_file = expanduser("~") + "/.rastreio.conf"
with open(config_file) as f: lines = f.readlines()
f.close()

for line in lines:
    if not re.match("^\s*#", line):
        output = lookup(line.rstrip('\n'))
        pretty_print(output)
