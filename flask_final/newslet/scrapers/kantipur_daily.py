"""
Script to scrape news from www.kantipurdaily.com/[news/world]
Contains:
    kantipur_daily_extractor(): Gives list of news dicts
 """
from bs4 import BeautifulSoup as BS
import requests

from common import get_soup, format_date


def kantipur_daily_extractor(endpoint='news'):
    """
    Extracts news from www.kantipurdaily.com/news
    Params: endpoints = {news, world}
    Returns:
    The order is as given by the website
    A list containing news dictionaries. Here is a sample

        {
            title: str in nepali
            'raw_date': 2019/06/34 like date,
            'source': 'ekantipur',
            'summary': news summary in nepali,
            'news_link': link,
            'image_link': imglink,
        }

    """
    url = f'https://www.kantipurdaily.com/{endpoint}'
    soup = get_soup(url)
    news_list = []
    for article in soup.find_all("article", class_="normal"):
        title = article.h2.a.text
        summary = article.find("p").text
        image = article.find("div", class_="image").figure.a.img["data-src"]
        img = image.replace("-lowquality", "")
        small_img = img.replace("lowquality", "")
        big_img = small_img.replace("300x0", "1000x0")
        date_ore = article.h2.a["href"]
        contaminated_list = date_ore.split("/")
        pure_date_list = [
            contaminated_list[2],
            contaminated_list[3],
            contaminated_list[4],
        ]
        date = "/".join(pure_date_list)
        link = "https://kantipurdaily.com" + date_ore
        date = format_date(date)
        news_dict = {
            "title": title,
            "raw_date": date,
            "source": "ekantipur",
            "summary": summary,
            "news_link": link,
            "image_link": big_img,
        }
        news_list.append(news_dict)

    return news_list

def kantipur_international_extractor:
    return kantipur_daily_extractor(endpoint='world')

if __name__ == "__main__":
    news = kantipur_daily_extractor()
    print(len(news))
