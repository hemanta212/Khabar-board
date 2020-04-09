# -*=Code = UTF-8
"""
Utils module to get news from extractor and register them with an order
to the database models.
Contains:
    load_news_to_models(): collects and registers news of specified category
"""

# Try catch block to make offline development possble
try:
    from flask_final.newslet.scrapers.kantipur_daily import (
        kantipur_daily_extractor, kantipur_international_extractor
    )
    from flask_final.newslet.scrapers.kathmandupost import kathmandu_post_extractor
    from flask_final.newslet.scrapers.nagarik import (
        nagarik_news_extractor,
    )
    from flask_final.newslet.top_international_news import get_general_headlines
    from flask_final.newslet.rss_news import get_news_from_rss

# Incase scrapers cannot be imported (networks or some reasons)
except Exception as E:
    print(E)

    def load_news_to_models(category):
        """
        Have an ineffective loader function
        just to prevent import errros
        """
        pass

    # Script terminates from here

# This else block is only runned if try block is succesful
else:
    from flask_final.newslet.models import NepNationalNews as NNN
    from flask_final.newslet.models import NepInternationalNews as NIN
    from flask_final.newslet.models import EngNationalNews as ENN
    from flask_final.newslet.models import EngInternationalNews as EIN
    from flask_final import db, NEWS_API_KEY

    def load_news_to_models(category):
        """
        Get news from scraper and registers to database model of
        associated given category
        Param: category (either of ['NIN','NNN','ENN'])
        Returns: Nothing, Once you call this funtion with specific
                category, you can use the updated models directly
        """
        models = {"NNN": NNN, "NIN": NIN, "ENN": ENN, "EIN": EIN}

        scrapers = {
            "NNN": (kantipur_daily_extractor,),
            "NIN": (kantipur_international_extractor, nagarik_international_extractor),
            "ENN": (kathmandu_post_extractor,),
        }

        extractors = {"EIN": ((get_general_headlines, NEWS_API_KEY, dict()),)}

        news_list = []
        if category in scrapers:
            for extractor in scrapers.get(category):
                news_list += extractor()
            if category == "ENN":
                for news in news_list:
                    pass

        else:
            for func_info in extractors.get(category):
                func, API_KEY, kwargs = func_info
                news_list = func(API_KEY, **kwargs)

        category_rss_map = {
            "NNN": ("ujyaalo_online", "hamra_kura"),
            "ENN": ("himalayan_times", "nepali_times"),
        }
        if category in category_rss_map:
            sources = category_rss_map[category]
            for source in sources:
                news_list += get_news_from_rss(source)
            print("NEWSLIST IS ", len(news_list))

        i = 0
        for news in reversed(news_list):
            # In scraped_news_list index 0 is latest one. This for loop
            # iterates in opposite direction so that
            # index 0 (latest news) is registered at last so that
            # it has newest date and the last item is registerd at first
            # so it gets oldest date assigned by db model
            duplicate = (
                models[category].query.filter_by(news_link=news["news_link"]).first()
            )

            if not duplicate:
                news_post = models[category](
                    title=news["title"],
                    source=news["source"],
                    summary=news["summary"],
                    image_link=news["image_link"],
                    news_link=news["news_link"],
                    raw_date=news["raw_date"],
                    date=news.get("date"),
                )
                db.session.add(news_post)
                db.session.commit()
                i += 1

        order = models[category].date.desc()
        print("Unique news", i)

        # this for loop picks iterates over latest news list
        # and then preserves first 100 items and deletes  all others
        for i in models[category].query.order_by(order)[100:]:
            db.session.delete(i)
            db.session.commit()
