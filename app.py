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


news_category = ""
redirect_to = ""

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
	global redirect_to
	if redirect_to == "profile":
		return redirect(url_for("profile"))
	else:
		return redirect(url_for("news_by_category", category = news_category))


# route to vote news ---
@app.route("/vote_news/<title>/<polarity>")
def vote_news(title, polarity):
	if current_user.is_authenticated:
		User = current_user
	else:
		return "{'error': 'Incorrect Credentials'}"
	response = User.vote_news(title, polarity)
	return "{'status': "+str(response)+"}"

@app.route("/get_votes/<title>")
def get_votes(title):
	data = News.getvotes(title)
	return jsonify(data)


@app.route("/profile")
def profile():

	if current_user.is_authenticated:
		User = current_user
	else:
		return redirect(url_for("login"))
	global redirect_to
	if redirect_to == "profile":
		save_note = "Saved Successfully"
	else:
		save_note = ""
	redirect_to == ""
	redirect_to = "profile"

	user_pref = User.get_preference()
	return render_template("profile.html", 
		user = User, 
		user_pref = user_pref,
		country_map = country_map,
		language_map = language_map,
		save_note = save_note
		)

@app.route("/news/<category>")
def news_by_category(category):
	# session handling
	if current_user.is_authenticated:
		User = current_user
	else:
		return redirect(url_for("login"))

	global news_category
	news_category = category

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
	
	return render_template("readnews.html", 
		data=loaded_news, user = User, 
		category = category.capitalize()+" News", 
		user_pref = user_pref,
		country_map = country_map,
		language_map = language_map
		)

#to start the flask server
if __name__ == '__main__':
	app.run(ssl_context = "adhoc")

