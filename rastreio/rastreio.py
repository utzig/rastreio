#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import os.path
import re
import sys
import requests

try:
    from html.parser import HTMLParser
except ImportError:
    from HTMLParser import HTMLParser

COMMENT = "^\s*#"

class TableParser(HTMLParser):
    """
    This class is used to parse the table data received back by the
    online lookup for each tracking code
    """
    def __init__(self):
        HTMLParser.reset(self)
        self.inside_table = False
        self.table_data = []
        self.rowspan = 1
        self.strict = False
        self.convert_charrefs = False

    def handle_starttag(self, tag, attrs):
        if tag == 'table':
            self.inside_table = True
            self.current_row = 0
            self.current_col = 0
        if self.inside_table:
            if tag == 'td':
                if len(attrs) > 0 and attrs[0][0] == 'rowspan':
                    self.rowspan = int(attrs[0][1])

    def handle_endtag(self, tag):
        if self.inside_table:
            if tag == 'tr':
                self.rowspan -= 1
                if self.rowspan == 0:
                    self.current_row += 1
                    self.current_col = 0
            elif tag == 'td':
                self.current_col += 1
        if tag == 'table':
            self.inside_table = False

    def handle_data(self, data):
        if self.inside_table and not re.match('\n', data):
            stripped_data = " ".join(data.split())
            if stripped_data != '':
                value = (self.current_row, self.current_col, stripped_data)
                self.table_data.append(value)


def lookup(tracking_code):
    """
    Receives the tracking code as string and does online search.
    Returns the html received from the page lookup
    """
    params = 'Z_ACTION=Search&P_TIPO=001&P_LINGUA=001&P_COD_UNI=' + tracking_code
    url = "http://websro.correios.com.br/sro_bin/txect01$.QueryList"
    return requests.post(url, params).text


def pretty_print(tracking_code, html_data):
    parser = TableParser()
    parser.feed(html_data)
    last_row = 1
    print(tracking_code + ':')
    if len(parser.table_data) > 0:
        for data in parser.table_data:
            row, col, text = data
            if row == 0: # ignoring the first row because it's header info...
                continue
            if last_row != row:
                print('')
                last_row = row
            if col == 0:
                xtext = "%s " % text
                sys.stdout.write(xtext)
            else:
                xtext = "| %s " % text
                sys.stdout.write(xtext)
        print('')
    else:
        print('O sistema não possui dados sobre o objeto informado.')
    print('')


def main():
    config_file = os.path.expanduser("~") + "/.rastreio.conf"
    try:
        with open(config_file) as f:
            lines = f.readlines()
        f.close()
    except IOError:
        print('Arquivo de entrada não encontrado!')
        sys.exit()

    for line in lines:
        if not re.match(COMMENT, line):
            tracking_code = line.rstrip('\n')
            response_html = lookup(tracking_code)
            pretty_print(tracking_code, response_html)


if __name__ == "__main__":
    main()