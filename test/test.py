from newsapi import NewsApiClient
from textblob import TextBlob

# # Init
newsapi = NewsApiClient(api_key='63d39c686718447fb0d1ccc422c98029')

# # /v2/top-headlines
top_headlines = newsapi.get_top_headlines(q='',language='en',country='in')

# # /v2/everything
print(top_headlines)

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

print(top_headlines["articles"][0])

#import spacy
#from spacytextblob.spacytextblob import SpacyTextBlob
#
#nlp = spacy.load('en_core_web_sm')
#nlp.add_pipe('spacytextblob')
#text = 'Nearly 300 dengue, viral fever patients admitted to hospital in Uttar Pradesh.'
#doc = nlp(text)
#print(doc._.polarity) # Polarity: -0.125
#print(doc._.subjectivity) # Sujectivity: 0.9
#print(doc._.assessments)  # Assessments: [(['really', 'horrible'], -1.0, 1.0, None), (['worst', '!'], -1.0, 1.0, None), (['really', 'good'], 0.7, 0.6000000000000001, None), (['happy'], 0.8, 1.0, None)]
#if(doc._.polarity<0):
#    print("negative")
#else:
#    print("positive")