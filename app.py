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

from Sentiment import sentiemnt_analyze, sentiemnt_analyze1

app =  Flask(__name__)
app.secret_key = os.urandom(24)

# google login implementation code

# google login secret keys 

#GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_ID = "533715066104-dhah0vhmvqf80g2dipia8nc89rkkfo1e.apps.googleusercontent.com"
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


# route to top headlines user redirected after login.
@app.route("/top_headlines")
def top_headlines():
	if current_user.is_authenticated:
		pass
	else:
		return redirect(url_for("login"))

	# to calculate last modified time of the news
	m = os.path.getmtime("allnews.json")  #in format 428574574534
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

	if(flag):
		with open("allnews.json","w") as all:
			#fetch news from newsapi.org
			newsapi = NewsApiClient(api_key='63d39c686718447fb0d1ccc422c98029')

			# # /v2/top-headlines endpoint
			top_headlines = newsapi.get_top_headlines(q='',language='en',country='in')

			#sentiment analysis for all fetched news
			top_headlines = sentiemnt_analyze(top_headlines)
			print("analysis by stanformd NLP")

			#over write new news to the allnews.json file
			all.write(json.dumps(top_headlines))
			print("new updated")


	allnews_json=None
	with open("allnews.json","r") as allnews:
		allnews_json = json.load(allnews)
		#print(allnews_json["articles"][0])
	User = current_user
	return render_template("readnews.html",data = allnews_json, user = User, category = "Top Headlines")

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
	if(flag):
		# code just test
		newsapi = NewsApiClient(api_key='63d39c686718447fb0d1ccc422c98029')


		# # /v2/top-headlines
		top_headlines = newsapi.get_top_headlines(category="sports", country="in")
		
		# sentiment analysis for all retrived news
		top_headlines = sentiemnt_analyze(top_headlines)

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
	return render_template("readnews.html",data=sports_news, user = User, category = "Sports News")


#to start the flask server
if __name__ == '__main__':
	app.run(ssl_context = "adhoc", debug=True)

