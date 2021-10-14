from textblob import TextBlob
import os
import numpy as np
import pandas as pd
import json
from pycorenlp import StanfordCoreNLP

def sentiemnt_analyze(top_headlines):
	i=0;
	for article in top_headlines["articles"]:
	    testimonial = TextBlob(article["title"].split("-")[0])
	    print(article["title"].split("-")[0])
	    if(testimonial.sentiment.polarity<0):
	        top_headlines["articles"][i]["sentiment"]="negative"
	    if(testimonial.sentiment.polarity == 0):
	    	top_headlines["articles"][i]["sentiment"]="neutral"
	    else:
	        top_headlines["articles"][i]["sentiment"]="positive"
	    i+=1
	return top_headlines;

nlp = StanfordCoreNLP('http://localhost:9000')
def stanford_sentiment(text_str):
	res = nlp.annotate(text_str, properties={'annotators': 'sentiment', 'outputFormat': 'json', 'timeout': 40000,})
	output = eval(res)
	return output["sentences"][0]["sentiment"]

def sentiemnt_analyze1(top_headlines):
	nlp = StanfordCoreNLP('http://localhost:9000')
	i=0;
	for article in top_headlines["articles"]:
		top_headlines["articles"][i]["sentiment"]=stanford_sentiment(article["title"].split("-")[0])
		i+=1
	return top_headlines;