from flask import Flask
from flask import render_template
from newsapi import NewsApiClient
from textblob import TextBlob
from flask import jsonify
import json
import os
import time
import datetime

app =  Flask(__name__)

@app.route("/")
def main():
	return render_template("index.html")

@app.route("/allnews")
def allnews():
	m = os.path.getmtime("allnews.json")  #428574574534
	#print(time.ctime(m))
	m = time.gmtime(m) #{}
	c = time.time()
	#print(time.ctime(c))
	c = time.gmtime(c)

	print(f"{m} \n {c}")
	print((c.tm_hour - m.tm_hour)*60+(c.tm_min - m.tm_min))

	flag=False
	if(c.tm_mday != m.tm_mday):
		flag = True
	if((c.tm_hour - m.tm_hour)*60+(c.tm_min - m.tm_min) >= 60):
		flag = True
	if(flag):
		with open("allnews.json","w") as all:
		
			newsapi = NewsApiClient(api_key='63d39c686718447fb0d1ccc422c98029')

			# # /v2/top-headlines
			top_headlines = newsapi.get_top_headlines(q='',language='en',country='in')

			# # /v2/everything
			# print(top_headlines["totalResults"])

			i=0;
			for article in top_headlines["articles"]:
			    testimonial = TextBlob(article["title"])
			    if(testimonial.sentiment.polarity<0):
			        top_headlines["articles"][i]["sentiment"]="negative"
			    else:
			        print("posiitive")
			        top_headlines["articles"][i]["sentiment"]="positive"
			    i+=1

			#print(top_headlines)
			# api call finished
			all.write(json.dumps(top_headlines))


	allnews_json=None
	with open("allnews.json","r") as allnews:
		allnews_json = json.load(allnews)
		#print(allnews_json["articles"][0])
	return render_template("readnews.html",data=allnews_json)

@app.route("/sports")
def soprts_news():
	m = os.path.getmtime("sports_news.json")
	#print(time.ctime(m))
	m = time.gmtime(m)
	c = time.time()
	#print(time.ctime(c))
	c = time.gmtime(c)

	print(f"{m} \n {c}")
	print((c.tm_hour - m.tm_hour)*60+(c.tm_min - m.tm_min))
	flag=False
	if(c.tm_mday != m.tm_mday):
		flag = True
	if((c.tm_hour - m.tm_hour)*60+(c.tm_min - m.tm_min) >= 60):
		flag = True
	if(flag):
		# code just test
		newsapi = NewsApiClient(api_key='63d39c686718447fb0d1ccc422c98029')

		# # /v2/top-headlines
		top_headlines = newsapi.get_top_headlines(category="sports", country="in")
		# api call finished
		with open("sports_news.json","w") as all:
			all.write(json.dumps(top_headlines))
			print("json updated")

	
	sports_news=None
	with open("sports_news.json","r") as sports:
		sports_news = json.load(sports)
		#print(sports_news["articles"][0])

	return render_template("readnews.html",data=sports_news)

if __name__ == '__main__':
	app.run(debug=True)

