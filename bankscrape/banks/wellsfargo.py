#!/usr/bin/env python
import logging
import ssl
import os, sys, re, StringIO, csv

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
from bankscrape.scraper import unescape_html

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARN)

class TLSv1Adapter(HTTPAdapter):
    """Force TLSv1

    Wells Fargo hangs with requests' default SSL setup so hard-set
    TLSv1 here.

    http://lukasa.co.uk/2013/01/Choosing_SSL_Version_In_Requests/

    """

    def init_poolmanager(self, connections, maxsize, **kwargs):
        self.poolmanager = PoolManager(num_pools=connections,
                                       maxsize=maxsize,
                                       ssl_version=ssl.PROTOCOL_TLSv1)


SCRAPER = requests.Session()
SCRAPER.mount('https://', TLSv1Adapter())

def login(username, password):
    SCRAPER.get('https://www.wellsfargo.com/')
    login_data = {
        'userid': username,
        'password': password,
        'screenid': 'SIGNON',
        'origination': 'WebCons',
        'LOB': 'Cons',
    }
    SCRAPER.post('https://online.wellsfargo.com/signon', login_data)
    response = SCRAPER.get('https://online.wellsfargo.com/das/cgi-bin/session.cgi?screenid=SIGNON_PORTAL_PAUSE')
    return response.text

def handle_stupid_online_statement_question(pagehtml):
    soup = BeautifulSoup(pagehtml)
    remindme_url = soup.find(name='input', attrs={'name': 'Considering'}).parent['action']
    data = {'Considering': 'Remind me later'}
    response = SCRAPER.post(remindme_url, data)
    return load_account_page(response.text, handle_error=False)

def load_account_page(mainpagehtml, handle_error=True):
    soup = BeautifulSoup(mainpagehtml)
    try:
        account_url = soup.find(name='a', attrs={'title': re.compile('Account Activity')})['href']
    except TypeError:
        if handle_error:
            logger.debug("handling stupid paperless statement question")
            return handle_stupid_online_statement_question(mainpagehtml)
        else:
            raise
    response = SCRAPER.get(account_url)
    return response.text

def col2entry(col):
    return unescape_html(col.contents[0].strip())

def parse_account_page(pagehtml):
    soup = BeautifulSoup(pagehtml)
    table = soup.find(name='table', attrs={'id': 'DDATransactionTable'})
    rows = table.find('tbody').findAll('tr')
    trans = list()
    for row in rows:
        tran = [col2entry(col) for col in row.findAll(recursive=False)]
        if len(tran) == 4:
            trans.append(tran)
    return trans

def transactions_to_csv(transactions):
    stringio = StringIO.StringIO()
    writer = csv.writer(stringio)
    writer.writerows(transactions)
    return stringio.getvalue()

def scrape(config_items):
    logging.basicConfig()

    username = config_items['username']
    password = config_items['password']

    logger.debug("logging in")
    main_page_html = login(username, password)
    logger.debug("loading account page")
    account_page_html = load_account_page(main_page_html)
    logger.debug("parsing transactions")
    transactions = parse_account_page(account_page_html)
    trans_csv = transactions_to_csv(transactions)
    return trans_csv
