from newsapi import NewsApiClient
import os
from dotenv import load_dotenv

load_dotenv()
api = NewsApiClient(api_key =os.getenv('NEWS_API_KEY'))



def sendNews(query):

    covidNews = api.get_everything(q=query, sort_by='relevancy', page=1)

    count = 5

    news_dict = {}
    for article in covidNews['articles']:
        print(article['title'])
        print(article['url'])
        news_dict[article['title']] = article['url']
        print('\n')

        count = count - 1
        if count == 0:
            break
    return news_dict

