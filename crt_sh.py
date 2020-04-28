from __future__ import print_function
try:
    import psycopg2
except ImportError:
    raise ImportError('\n\033[33mpsycopg2 library missing. pip install psycopg2\033[1;m\n')
    sys.exit(1)

try:
    import click
except ImportError:
    raise ImportError('\n\033[33mclick library missing. pip install click\033[1;m\n')
    sys.exit(1)
import re
import sys
import json
import logging
from os.path import abspath


class CRTsh():
    def __init__(self, args, target, handler):
        self.description = "CRT.sh Module"
        self.author      = '@ahmetumitbayram'
        self.method      = ['scrape']

        self.handler     = handler
        self.target      = target

    def execute(self):
        logging.basicConfig(
            level=logging.INFO,
            format="%(message)s"
            )

        DB_HOST = 'crt.sh'
        DB_NAME = 'certwatch'
        DB_USER = 'guest'
        DB_PASSWORD = ''


        try:
            conn = psycopg2.connect("dbname={0} user={1} host={2}".format(DB_NAME, DB_USER, DB_HOST))
            conn.autocommit = True
            cursor = conn.cursor()
            cursor.execute("SELECT ci.NAME_VALUE NAME_VALUE FROM certificate_identity ci WHERE ci.NAME_TYPE = 'dNSName' AND reverse(lower(ci.NAME_VALUE)) LIKE reverse(lower('%{}'));".format(self.target))
        except:
            logging.info("\n\033[1;31m[!] Unable to connect to the database\n\033[1;m")



        unique_domains = []
        for result in cursor.fetchall():
            matches=re.findall(r"\'(.+?)\'",str(result))
            for subdomain in matches:
                if subdomain not in unique_domains:
                    if ".{}".format(self.target) in subdomain:
                        unique_domains.append(subdomain)
        for sub in unique_domains:
            self.handler.sub_handler({'Name': sub, 'Source': 'CRT-sh'})
