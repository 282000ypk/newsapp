import json
import psycopg2
from newsapi import NewsApiClient
from cred import NEWS_API_KEY

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

		cursor.execute("select sum(positive_vote), sum(negative_vote) from news where news_id = '"+news+"'")
		all_votes = cursor.fetchone()
		if all_votes[0] != None:
			votes = {
				"positive_vote": all_votes[0],
				"negative_vote": all_votes[1]
			}
		else:
			votes = {
				"positive_vote": 0,
				"negative_vote": 0
			}
		return votes

	@staticmethod
	def getvotes(news):
		#connect to DB
		conn = psycopg2.connect(
    		host="localhost",
    		database="smartnewsapp",
    		user="postgres",
    		password="postgres")

		cursor = conn.cursor()
		cursor.execute("delete from news")
		cursor,execute("commit")

	@staticmethod
	def search_news(query):
		newsapi = NewsApiClient(api_key=NEWS_API_KEY)
		news = newsapi.get_everything(q=query)
		return news

	@staticmethod
	def get_top_headlines(language, country):
		newsapi = NewsApiClient(api_key=NEWS_API_KEY)
		news = newsapi.get_top_headlines(language=language, country=country)
		return news

	@staticmethod
	def get_news_by_category(category, language, country):
		newsapi = NewsApiClient(api_key=NEWS_API_KEY)
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


