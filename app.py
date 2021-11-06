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
from country_language import country_map, language_map

app =  Flask(__name__)
app.secret_key = os.urandom(24)

# google login implementation code

# google login secret keys 

#GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
#GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_CLIENT_SECRET = "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"
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"

news_category = ""

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
		return redirect(url_for("news_by_category", category = "top_headlines"))
	else:
		return render_template("index.html")


def get_google_provider_cfg():
	return requests.get(GOOGLE_DISCOVERY_URL).json()

#routes for google login 

#redirect user to google login page.
@app.route("/login")
def login():
	if current_user.is_authenticated:
		return redirect(url_for("news_by_category", category = "top_headlines"))
	else:
		pass

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
	login_user(user)
	if not temp_user:
		User.create(unique_id, users_name, users_email, picture)

	else:
		if(temp_user.user_type == 'ADMIN'):
			return redirect(url_for("admin"))
	

	return redirect(url_for("news_by_category", category = "top_headlines"))

#route to logout user.
@app.route("/logout")
@login_required
def logout():
	logout_user()
	print("logged out")
	return redirect(url_for("main"))

@app.route("/admin")
def admin():
	if current_user.is_authenticated:
		pass
	else:
		return render_template("index.html")
	return render_template("admin.html")

@app.route("/admin_dashboard")
def admin_dashboard():
	if current_user.is_authenticated:
		pass
	else:
		return render_template("index.html")
	return render_template("admin.html")
	users = User.get_all()
	return render_template("admin_dashboard.html", data = users)

# route to set laguage and country
@app.route("/change_preference/", methods = ['POST', 'GET'])
def change_preference():
	if current_user.is_authenticated:
		pass
	else:
		return redirect(url_for("main"))
	if request.method == 'POST' :
		language = request.args["language"]
		country = request.args["country"]
	else:
		print(request.form.items())
		language = request.args["language"]
		country = request.args["country"]
	user = current_user
	user.set_preference(language, country)
	return redirect(url_for("news_by_category", category = news_category))


# route to vote news ---
@app.route("/vote_news/<title>/<polarity>")
def vote_news(title, polarity):
	print(title, polarity)
	user = current_user
	response = user.vote_news(title, polarity)
	return "{'status': "+str(response)+"}"

@app.route("/get_votes/<title>")
def get_votes(title):
	print(title)
	data = News.getvotes(title)
	return jsonify(data)


@app.route("/news/<category>")
def news_by_category(category):
	# session handling
	if current_user.is_authenticated:
		User = current_user
	else:
		return render_template("index.html")

	m = os.path.getmtime(category+".json")
	m = time.gmtime(m)
	
	c = time.time()
	c = time.gmtime(c)
	global news_category
	news_category = category

	print(f"{m} \n {c}")
	print((c.tm_hour - m.tm_hour)*60+(c.tm_min - m.tm_min))
	flag=False
	if(c.tm_mday != m.tm_mday):
		flag = True
	if((c.tm_hour - m.tm_hour)*60+(c.tm_min - m.tm_min) >= 60):
		flag = True
	# to force updating news
	flag = True

	if(not flag):
		with open(category+".json","r") as news:
			try:
				loaded_news = json.load(news)
				print("loaded")
			except:
				flag = True

	if(flag):
		with open(category+".json","w+") as all:
			#fetch news from newsapi.org using news.py
			user_pref = User.get_preference()
			print(user_pref)
			if category == "top_headlines":
				loaded_news = News.get_top_headlines(user_pref[0],user_pref[1])	
			else:
				loaded_news = News.get_news_by_category(category,user_pref[0],user_pref[1])
			# clear votes as news are refreshed
			# News.clearvotes()

			# sentiment analysis for all fetched news by TextBlob
			loaded_news = sentiemnt_analyze(loaded_news)

			# analysis by stanform analysis algorithm.
			# top_headlines = sentiemnt_analyze1(top_headlines)
			# print("analysis by stanformd NLP")

			#over write new news to the appropriate .json file
			all.write(json.dumps(loaded_news))
			print("new updated")




	
	return render_template("readnews.html", 
		data=loaded_news, user = User, 
		category = category.capitalize()+" News", 
		user_pref = user_pref,
		country_map = country_map,
		language_map = language_map
		)

#to start the flask server
if __name__ == '__main__':
	app.run(ssl_context = "adhoc", debug=True)

