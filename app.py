from flask import Flask
from flask import render_template
from newsapi import NewsApiClient
from textblob import TextBlob

app =  Flask(__name__)
 
@app.route("/")
def main():
	return render_template("index.html")

@app.route("/readnews")
def readnews():
	

	# # Init
	newsapi = NewsApiClient(api_key='63d39c686718447fb0d1ccc422c98029')

	# # /v2/top-headlines
	top_headlines = newsapi.get_top_headlines(q='',language='en',country='in')

	# # /v2/everything
	# print(top_headlines["totalResults"])

	i=0;
	for article in top_headlines["articles"]:
	    testimonial = TextBlob(article["title"])
	    if(testimonial.sentiment.polarity<0):
	        print("negative")
	        top_headlines["articles"][i]["sentiment"]="negative"
	    else:
	        print("posiitive")
	        top_headlines["articles"][i]["sentiment"]="positive"
	    i+=1
	# print(top_headlines["articles"][0])

	return render_template("readnews.html",data=top_headlines)

if __name__ == '__main__':
	app.run(debug=True)

