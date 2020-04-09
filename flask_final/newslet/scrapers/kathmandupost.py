"""
Script to scrape news from kathmandupost.ekantipur.com
Contains:
    kathmandu_post_extractor(): Gives list of news dicts
 """

from bs4 import BeautifulSoup as BS
import requests

from common import get_soup, format_date

def kathmandu_post_extractor():
    """Extracts the news from https://kathmandupost.ekantipur.com
       with the same order as that of the website
    Retruns:
        A list containing dictionaries of news list[0] has latest
        example of such dictionary is
        {
                "image_link": image_link,
                "title": title in englist,
                "raw_date": date in 23 Mar 2018 format,
                "source": "ekantipur",
                "news_link": full_link,
                "summary": summary,
        }

    """
    url = 'https://kathmandupost.ekantipur.com'
    soup = get_soup(url)
    news_list = []
    column_one = soup.find("div", class_="grid-first")
    column_two = soup.find("div", class_="grid-second")
    column_three = soup.find("div", class_="grid-third")
    latest_column = soup.find("div", class_="block--morenews")
    sources = [column_one, column_two, column_three, latest_column]

    for column in sources:
        articles = column.find_all("article")

        if column == column_two:
            featured_article = articles[0]
            h3_tag = soup.new_tag("h3")
            featured_article.h2.wrap(h3_tag)
            featured_article.h3.h2.unwrap()

        elif column == latest_column:
            for article in articles:
                a_tag = article.a
                a_tag.string = article.h3.string
                article.h3.insert(0, a_tag)

        for article in articles:
            href_link = article.h3.a["href"]
            article_link = url + href_link
            title = article.h3.a.text

            raw_date = "/".join(href_link.split("/")[2:5])
            date = format_date(raw_date)
            print(date)

            image_tag = article.find("img")
            if image_tag:
                image_link = image_tag["data-src"]
            else:
                image_link = None

            summary = article.p.text

            news_dict = {
                "title": title,
                "source": "ekantipur",
                "news_link": article_link,
                "raw_date": date,
                "summary": summary,
                "image_link": image_link,
            }

            news_list.append(news_dict)

    return news_list


if __name__ == "__main__":
    news = kathmandu_post_extractor()
    print(len(news))
