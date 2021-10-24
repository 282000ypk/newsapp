import json
import psycopg2
from newsapi import NewsApiClient

class News():
	def __init__(self, title, positive_vote, negative_vote, ):
		self.title = title
		self.positive_vote = positive_vote
		self.negative_vote = negative_vote

	@staticmethod
	def getvotes(news):
		#connect to DB
		conn = psycopg2.connect(
    		host="localhost",
    		database="smartnewsapp",
    		user="postgres",
    		password="postgres")

		cursor = conn.cursor()

		i=0;
		for article in top_headlines["articles"]:
			cursor.execute("select sum(positive_vote), sum(negative_vote) from news where title = '"+news["articles"][i]["title"]+"'")
			all_votes = cursor.fetchone()
			news["articles"][i]["positive_vote"] = all_votes[0]
			news["articles"][i]["negative_vote"] = all_votes[1]
			i+=1
		
		return news

	@staticmethod
	def search_news(query):
		newsapi = NewsApiClient(api_key='63d39c686718447fb0d1ccc422c98029')
		news = newsapi.get_everything(q=query)
		return news

	@staticmethod
	def get_top_headlines(language, country):
		newsapi = NewsApiClient(api_key='63d39c686718447fb0d1ccc422c98029')
		news = newsapi.get_top_headlines(language=language, country=country)
		return news

	@staticmethod
	def get_news_by_category(category, country, language):
		newsapi = NewsApiClient(api_key='63d39c686718447fb0d1ccc422c98029')
		news = newsapi.get_top_headlines(category = category, country = country, language = language)
		return news


	@staticmethod
	def readfromjson(category):
		pass
		# if category == "sports":
		# 	with open("sports_news.json","r") as sports:
		# 	sports_news = json.load(sports)
		# if category == "top_headlines":
		# 	with open("allnews.json","r") as allnews:
		# 	allnews_json = json.load(allnews)

			

if __name__ == '__main__':
	print(News.getvotes())
	print()


