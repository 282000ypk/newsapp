from flask import Flask, redirect, request, url_for
from flask import render_template
from newsapi import NewsApiClient
from textblob import TextBlob
from flask import jsonify
import json
import os
import time
import datetime
from oauthlib.oauth2 import WebApplicationClient
import requests
from user import User
from flask_login import (LoginManager, current_user, login_required, login_user, logout_user)
from news import News
from Sentiment import sentiemnt_analyze, sentiemnt_analyze1
from cred import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_DISCOVERY_URL

app =  Flask(__name__)
app.secret_key = os.urandom(24)

# google login implementation code

# google login secret keys 

#GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
#GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_CLIENT_SECRET = "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"
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"


login_manager = LoginManager()
login_manager.init_app(app)

client = WebApplicationClient(GOOGLE_CLIENT_ID)

@login_manager.user_loader
def load_user(user_id):
	return User.get(user_id)

@app.route("/")
def main():
	# session handling
	if current_user.is_authenticated:
		return redirect(url_for("top_headlines"))
	else:
		return render_template("index.html")


def get_google_provider_cfg():
	return requests.get(GOOGLE_DISCOVERY_URL).json()

#routes for google login 

#redirect user to google login page.
@app.route("/login")
def login():
	google_provider_cfg = get_google_provider_cfg()
	authorization_endpoint = google_provider_cfg["authorization_endpoint"]
	request_uri = client.prepare_request_uri(authorization_endpoint, redirect_uri = request.base_url + "/callback", scope = ["openid", "email", "profile"])
	print(request_uri)
	return redirect(request_uri)

# response received from google as callback
@app.route("/login/callback")
def callback():
	code = request.args.get("code")
	print(code)
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
	user = User(id_ = unique_id, name = users_name, email = users_email, profile_pic_url = picture, user_type = "USER")
	
	temp_user = User.get(unique_id)
	redirect_to = "top_headlines"

	if not temp_user:
		User.create(unique_id, users_name, users_email, picture)
		redirect_to = "top_headlines"
	else:
		if(temp_user.user_type == 'ADMIN'):
			redirect_to = "admin"
	login_user(user)
	return redirect(url_for(redirect_to))

#route to logout user.
@app.route("/logout")
@login_required
def logout():
	logout_user()
	print("logged out")
	return redirect(url_for("main"))

@app.route("/admin")
def admin():
	return render_template("admin.html")

@app.route("/admin_dashboard")
def admin_dashboard():
	users = User.get_all()
	return render_template("admin_dashboard.html", data = users)

@app.route("/change_preference/", methods = ['POST', 'GET'])
def change_preference():
	if request.method == 'POST' :
		language = request.form["language"]
		country = request.form["country"]
	else:
		language = request.form["language"]
		country = request.form["country"]
	user = current_user
	user.set_preference(language, country)

@app.route("/vote_news/<title>/<polarity>")
def vote_news(title, polarity):
	print(title, polarity)
	user = current_user
	response = user.vote_news(title, polarity)
	return "{'status': "+str(response)+"}"

# route to top headlines user redirected after login.
@app.route("/top_headlines")
def top_headlines():
	if current_user.is_authenticated:
		pass
	else:
		return redirect(url_for("login"))

	# to calculate last modified time of the news
	m = os.path.getmtime("json/top_headlines.json")  #in format 428574574534
	m = time.gmtime(m) #{} #convert format
	c = time.time()
	c = time.gmtime(c)
	# to check if news are updated wihthin last 1 hour or not if not updated set flag to True
	flag=False
	if(c.tm_mday != m.tm_mday):
		flag = True
	if((c.tm_hour - m.tm_hour)*60+(c.tm_min - m.tm_min) >= 60):
		flag = True
	
	# to force fetching and analysing news
	# flag = True

	top_headlines=None
	if(flag):
		with open("top_headlines.json","w") as all:
			#fetch news from newsapi.org using news.py
			top_headlines = News.get_top_headlines("en","in")

			#sentiment analysis for all fetched news
			top_headlines = sentiemnt_analyze(top_headlines)

			#top_headlines = sentiemnt_analyze1(top_headlines)
			#print("analysis by stanformd NLP")

			#over write new news to the allnews.json file
			all.write(json.dumps(top_headlines))
			print("new updated")


	if(not flag):
		with open("top_headlines.json","r") as allnews:
			top_headlines = json.load(allnews)

	User = current_user
	return render_template("readnews.html",data = top_headlines, user = User, category = "Top Headlines")

@app.route("/sports")
def sports_news():
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
	# to force updating news
	# flag = True

	sports_news = None

	if(flag):
		with open("sports_news.json","w") as all:
			#fetch news from newsapi.org using news.py
			sports_news = News.get_news_by_category("sports","in","en")

			#sentiment analysis for all fetched news
			sports_news = sentiemnt_analyze(sports_news)

			#top_headlines = sentiemnt_analyze1(top_headlines)
			#print("analysis by stanformd NLP")

			#over write new news to the sports_news.json file
			all.write(json.dumps(sports_news))
			print("new updated")


	if(not flag):
		with open("sports_news.json","r") as sports_news:
			sports_news = json.load(sports_news)

	User = current_user
	return render_template("readnews.html",data=sports_news, user = User, category = "Sports News")

@app.route("/news/<category>")
def news_by_category(category):
	# session handling
	if current_user.is_authenticated:
		pass
	else:
		return render_template("index.html")

	m = os.path.getmtime(category+".json")
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
	# to force updating news
	# flag = True

	sports_news = None

	if(flag):
		with open(category+".json","w") as all:
			#fetch news from newsapi.org using news.py
			loaded_news = News.get_news_by_category(category,"in","en")

			#sentiment analysis for all fetched news
			loaded_news = sentiemnt_analyze(loaded_news)

			#top_headlines = sentiemnt_analyze1(top_headlines)
			#print("analysis by stanformd NLP")

			#over write new news to the sports_news.json file
			all.write(json.dumps(loaded_news))
			print("new updated")


	if(not flag):
		with open(category+".json","r") as news:
			loaded_news = json.load(news)
			print("loaded")

	User = current_user
	return render_template("readnews.html",data=loaded_news, user = User, category = category+"News")

#to start the flask server
if __name__ == '__main__':
	app.run(ssl_context = "adhoc", debug=True)

