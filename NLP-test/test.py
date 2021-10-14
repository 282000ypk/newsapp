import os
import numpy as np
import pandas as pd
import json
from pycorenlp import StanfordCoreNLP

nlp = StanfordCoreNLP('http://localhost:9000')

def stanford_sentiment(text_str):
    res = nlp.annotate(text_str,
                   properties={
                       'annotators': 'sentiment',
                       'outputFormat': 'json',
                       'timeout': 40000,
                   })
    output = eval(res)
    print(output["sentences"][0]["sentiment"])
    # numSentence = len(res)
    # numWords = len(text_str.split())
    
    # # data arrangement
    # arraySentVal = np.zeros(numSentence)

    # for i, s in enumerate(res["sentences"]):
    #     arraySentVal[i] = int(s["sentimentValue"])

    # # sum of sentiment values 
    # totSentiment = sum(arraySentVal)

    # # avg. of sentiment values 
    # avgSentiment = np.mean(arraySentVal)

    # # frequency of sentimentValue
    # bins = [0,1,2,3,4,5,6]
    # freq = np.histogram(arraySentVal, bins)[0]    # getting freq. only w/o bins
    #sentimentValue": "1","sentiment": "Negative","sentimentDistribution
    # return(numSentence, numWords, totSentiment, avgSentiment, freq)
with open("allnews.json","r") as f:
	news = json.load(f)
	for i in news["articles"]:
		stanford_sentiment(i["title"])