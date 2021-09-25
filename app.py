from flask import Flask
from flask import render_template
from newsapi import NewsApiClient
from textblob import TextBlob
from flask import jsonify
import json
import os

app =  Flask(__name__)
 
with open("allnews.json","w") as all:
	# # Init
	newsapi = NewsApiClient(api_key='63d39c686718447fb0d1ccc422c98029')

	# # /v2/top-headlines
	top_headlines = newsapi.get_everything(q='',language='en',country='in')

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

	print(top_headlines)
	all.write(json.dumps(top_headlines))
	

@app.route("/")
def main():
	return render_template("index.html")

@app.route("/allnews")
def allnews():
	last_modified = os.path.getmtime("allnews.json")
	print(last_modified)
	allnews_json=None
	with open("allnews.json","r") as allnews:
		allnews_json = json.load(allnews)
		print(allnews_json["articles"][0])
	return render_template("readnews.html",data=allnews_json)

if __name__ == '__main__':
	app.run(debug=True)

