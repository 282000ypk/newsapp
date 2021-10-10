from flask import Flask, redirect, request, url_for
from flask import render_template
from newsapi import NewsApiClient
from textblob import TextBlob
from flask import jsonify
import json
import os
import time
import datetime
import sqlite3
from oauthlib.oauth2 import WebApplicationClient
import requests
from db import init_db_command
from user import User
from flask_login import (LoginManager, current_user, login_required, login_user, logout_user)

app =  Flask(__name__)
app.secret_key = os.urandom(24)

# google login implementation code
#GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_ID = "533715066104-dhah0vhmvqf80g2dipia8nc89rkkfo1e.apps.googleusercontent.com"
#GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_CLIENT_SECRET = "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"
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"


login_manager = LoginManager()
login_manager.init_app(app)

try:
	init_db_command()
	print("db created")
except sqlite3.OperationalError:
	print("already created")

client = WebApplicationClient(GOOGLE_CLIENT_ID)

@login_manager.user_loader
def load_user(user_id):
	return User.get(user_id)

@app.route("/")
def main():
	# session handling
	if current_user.is_authenticated:
		return redirect(url_for("allnews"))
	else:
		return render_template("index.html")


def get_google_provider_cfg():
	return requests.get(GOOGLE_DISCOVERY_URL).json()

#routes for google login 
# route 1
@app.route("/login")
def login():
	google_provider_cfg = get_google_provider_cfg()
	authorization_endpoint = google_provider_cfg["authorization_endpoint"]
	request_uri = client.prepare_request_uri(authorization_endpoint, redirect_uri = request.base_url + "/callback", scope = ["openid", "email", "profile"])
	return redirect(request_uri)

@app.route("/login/callback")
def callback():
	code = request.args.get("code")
	google_provider_cfg = get_google_provider_cfg()
	token_endpoint = google_provider_cfg["token_endpoint"]
	token_url, headers, body = client.prepare_token_request(
		token_endpoint,
		authorization_response = request.url,
		redirect_url = request.base_url,
		code = code
		)
	token_response = requests.post(
		token_url,
		headers = headers,
		data = body,
		auth = (GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET)
		)
	client.parse_request_body_response(json.dumps(token_response.json()))
	userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
	url, header, body = client.add_token(userinfo_endpoint)
	userinfo_response = requests.get(url,headers = header, data = body)
	if(userinfo_response.json().get("email_verified")):
		unique_id = userinfo_response.json()["sub"]
		users_email = userinfo_response.json()["email"]
		picture = userinfo_response.json()["picture"]
		users_name = userinfo_response.json()["given_name"]
	else:
		return "User email not available or not verified by google", 400
	user = User(id_ = unique_id, name = users_name, email = users_email, profile_pic_url = picture)
	print(user)
	if not User.get(unique_id):
		User.create(unique_id, users_name, users_email, picture)

	login_user(user)
	return redirect(url_for("allnews"))

#route yo logout user.
@app.route("/logout")
@login_required
def logout():
	logout_user()
	print("logged out")
	return redirect(url_for("main"))


# route to all news user redirected after login.
@app.route("/allnews")
def allnews():
	# session handling
	if current_user.is_authenticated:
		pass
	else:
		return redirect(url_for("login"))

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
			print("new updated")


	allnews_json=None
	with open("allnews.json","r") as allnews:
		allnews_json = json.load(allnews)
		#print(allnews_json["articles"][0])
	User = current_user
	return render_template("readnews.html",data = allnews_json, user = User)

@app.route("/sports")
def soprts_news():
	# session handling
	if current_user.is_authenticated:
		pass
	else:
		return render_template("index.html")

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
		
		# sentiment analysis for all retrived news
		i=0;
		for article in top_headlines["articles"]:
		    testimonial = TextBlob(article["title"])
		    if(testimonial.sentiment.polarity<0):
		        top_headlines["articles"][i]["sentiment"]="negative"
		    else:
		        print("posiitive")
		        top_headlines["articles"][i]["sentiment"]="positive"
		    i+=1
		# write to json file on server    		
		with open("sports_news.json","w") as all:
			all.write(json.dumps(top_headlines))
			print("json updated")
	# retriving from local json  file on server
	sports_news=None
	with open("sports_news.json","r") as sports:
		sports_news = json.load(sports)
		#print(sports_news["articles"][0])
	User = current_user
	return render_template("readnews.html",data=sports_news, user = User)


#to start the flask server
if __name__ == '__main__':
	app.run(ssl_context = "adhoc", debug=True)

