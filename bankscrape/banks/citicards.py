#!/usr/bin/env python
import os, sys, re, StringIO, csv
from datetime import datetime

from BeautifulSoup import BeautifulSoup
import requests

SCRAPER = requests.session()

def login(username, password):
    response = SCRAPER.get('https://www.citicards.com/cards/wv/home.do')
    login_data = {
        'USERNAME': username,
        'PASSWORD': password,
        'NEXT_SCREEN': '/UnbilledTrans',
        'siteId': 'CB',
        'cookie_domain': 'citicards',
    }
    response = SCRAPER.post('https://www.accountonline.com/cards/svc/Login.do', login_data)
    # remove weird javascript that breaks beautiful soup
    html = response.text.replace('</fo"+"nt>', '')
    html = html.replace('_msg3: "</font>"', '')
    html = html.replace('_msg3: "</ul>"', '')
    html = html.replace('_msg3: "</p>"', '')
    return html

def parse_account_page(pagehtml):
    soup = BeautifulSoup(pagehtml)
    trans = get_transactions('unbilled')
    date_select = soup.find(id='date-select')
    last_date = date_select.find(value='1').contents[0]
    trans += get_transactions(last_date)
    return trans

def parse_date(datestr):
    try:
        return datetime.strptime(datestr, "%m/%d/%Y").date()
    except ValueError:
        d = datetime.strptime(datestr, "%m/%d").date()
        today = datetime.today()
        if d.month <= today.month:
            year = today.year
        else:
            year = today.year - 1
        return datetime(year, d.month, d.day).date()

def get_transactions(date):
    response = SCRAPER.get('https://www.accountonline.com/cards/svc/StatementDownload.do?dateRange=%s&viewType=csv' % date)
    trans = []
    for line in response.text.splitlines():
        tran = line.split('\t')
        if len(tran) < 3:
            continue
        trans_date, amount, desc = [d.strip() for d in tran[:3]]
        trans_date = parse_date(trans_date)
        trans.append([trans_date, desc, amount])
    trans.sort(cmp=lambda x,y: cmp(x[0], y[0]))
    trans.reverse()
    trans = [[datetime.strftime(t[0], "%m/%d/%Y"), t[1], t[2]] for t in trans]
    return trans

def transactions_to_csv(transactions):
    stringio = StringIO.StringIO()
    writer = csv.writer(stringio)
    writer.writerows(transactions)
    return stringio.getvalue()

def scrape(config_items):
    username = config_items['username']
    password = config_items['password']

    account_page_html = login(username, password)
    transactions = parse_account_page(account_page_html)
    trans_csv = transactions_to_csv(transactions)
    return trans_csv
