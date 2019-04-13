# -*=Code = UTF-8
'''
Utils module to get news from extractor and register them with an order
to the database models.
Contains:
    news_fetcher(): collects and registers news of specified category
'''

# Try catch block to make orffline development possble
try:
    from flask_final.newslet.kantipur_international import (
        kantipur_international_extractor)
    from flask_final.newslet.kantipur_daily import (
        kantipur_daily_extractor)
    from flask_final.newslet.kathmandupost import (
        kathmandu_post_extractor)

# Incase scrapers cannot be imported (networks or some reasons)
except Exception as E:
    print(E)

    def news_fetcher(category):
        '''
        Have an ineffective news_fetcher function
        just to prevent import errros
        '''
        pass
    # Script terminates from here

# This else block is only runned if try block is succesful
else:
    from flask_final.newslet.models import NepNationalNews as NNN
    from flask_final.newslet.models import NepInternationalNews as NIN
    from flask_final.newslet.models import EngNationalNews as ENN
    from flask_final import db

    def news_fetcher(category):
        '''
        Get news from scraper and registers to database model of
        associated given category
        Param: category (either of ['NIN','NNN','ENN'])
        Returns: Nothing, Once you call this funtion with specific
                category, you can use the updated models directly
        '''
        models = {
            'NNN': NNN,
            'NIN': NIN,
            'ENN': ENN,
        }

        extractors = {
            'NNN': kantipur_daily_extractor,
            'NIN': kantipur_international_extractor,
            'ENN': kathmandu_post_extractor,
        }

        scraped_news_list = extractors[category]()

        for news in scraped_news_list[::-1]:
            # In scraped_news_list index 0 is latest one. This for loop
            # iterates in opposite direction so that
            # index 0 (latest news) is registered at last so that
            # it has newest date and the last item is registerd at first
            # so it gets oldest date assigned by db model

            duplicate = models[category].query.filter_by(
                                                title=news["title"]).first()

            if duplicate is None:
                news_post = models[category](
                    title=news['title'],
                    source=news['source'], summary=news['summary'],
                    image_link=news['image_link'], news_link=news['news_link'],
                    nep_date=news["nep_date"])

                db.session.add(news_post)
                db.session.commit()

        if category != 'ENN':
            # use nep_date to order if english otherwise use date
            order = models[category].date.desc()  # order by latest news
        else:
            order = models[category].nep_date.desc()

        # this for loop picks iterates over latest news list
        # and then preserves first 60 items and deletes  all others
        for i in models[category].query.order_by(order)[60:]:
            db.session.delete(i)
            db.session.commit()
