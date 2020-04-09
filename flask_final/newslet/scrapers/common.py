from datetime import datetime
from bs4 import BeautifulSoup as BS
import requests


try:
    from flask_final.newslet import parser
except ImportError:
    parser = "lxml"

def get_soup(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36\
         (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    try:
        page = requests.get(url, headers=headers)
    except Exception as e:
        print("Connection refused by the server..", e)

    response = requests.get(url, headers=headers)
    soup = BS(response.content, parser)
    return soup


def format_date(raw_date):
    org_format = "%Y/%m/%d"
    datetime_obj = datetime.strptime(raw_date, org_format)
    dest_format = "%d %b %Y"
    date = datetime_obj.strftime(dest_format)
    return date
