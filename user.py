import json
import psycopg2
from flask_login import UserMixin

class User(UserMixin):
	def __init__(self, id_, name, email, profile_pic_url, user_type):
		self.id = id_
		self.name = name
		self.email = email
		self.profile_pic_url = profile_pic_url
		self.user_type= user_type

	@staticmethod
	def get(user_id):
		#connect to DB
		conn = psycopg2.connect(
    		host="localhost",
    		database="smartnewsapp",
    		user="postgres",
    		password="postgres")

		cursor = conn.cursor()
		cursor.execute("select * from newsapp_user where id = '"+user_id+"'")
		user = cursor.fetchone()

		if not user:
			return None

		user = User(id_ = user[0],name = user[1], email = user[2], profile_pic_url = user[3], user_type = user[4])

		return user

	@staticmethod
	def create(id_, name, email, profile_pic_url):
		query = "insert into newsapp_user values('"+id_+"',"+"'"+name+"',"+"'"+email+"',"+"'"+profile_pic_url+"',"+"'USER')"
		conn = psycopg2.connect(
    		host="localhost",
    		database="smartnewsapp",
    		user="postgres",
    		password="postgres")
		#user = db.execute("select * from newsapp_user where id= ?", (user_id,)).fetchone()

		cursor = conn.cursor()
		cursor.execute(query)
		cursor.execute("commit")


	@staticmethod
	def get_all():
		conn = psycopg2.connect(
    		host="localhost",
    		database="smartnewsapp",
    		user="postgres",
    		password="postgres")
		#user = db.execute("select * from newsapp_user where id= ?", (user_id,)).fetchone()

		cursor = conn.cursor()
		cursor.execute("select * from newsapp_user")
		all_user = cursor.fetchall()
		users=[]
		
		for user in all_user:
			user = User(id_ = user[0],name = user[1], email = user[2], profile_pic_url = user[3], user_type = user[4])
			users.append(user)
		return users

	def get_Preference():
		#connect to DB
		conn = psycopg2.connect(
    		host="localhost",
    		database="smartnewsapp",
    		user="postgres",
    		password="postgres")

		cursor = conn.cursor()
		cursor.execute("select language, country from user_preference where id = '"+self.id+"'")
		preference = cursor.fetchone()
		return preference

	def set_Preference(language, country):
		if not self.get_Preference():
			query = "insert into user_preference values('"+self.id+"','"+language+"','"+country+"')"
		else:
			query = "update user_preference set language='"+language+"', country='"+country+"' where id='"+self.id+"'"
		#connect to DB
		conn = psycopg2.connect(
    		host="localhost",
    		database="smartnewsapp",
    		user="postgres",
    		password="postgres")

		cursor = conn.cursor()
		cursor.execute(query)
		cursor.execute("commit")

	def check_vote(self, title):
		query = "select * from news where title = '"+title+"' and user_id='"+self.id+"'"
		conn = psycopg2.connect(
    		host="localhost",
    		database="smartnewsapp",
    		user="postgres",
    		password="postgres")

		cursor = conn.cursor()
		cursor.execute(query)
		vote = cursor.fetchone()
		if not vote:
			return False
		else:
			print("news found")
			return True	


	def vote_news(self, title, polarity):
		title = title.replace("'","''")
		title = title.replace("\"","''")
		if polarity=="positive":
			positive = 1
			negative = 0
		if polarity=="negative":
			positive = 0
			negative = 1
		if not self.check_vote(title):
			query = "insert into news values('"+title+"', "+str(positive)+","+str(negative)+", '"+self.id+"')"
		else:
			query = "update news set positive_vote = "+str(positive)+", negative_vote = "+str(negative)+" where user_id = '"+self.id+"' and title = '"+title+"'"
		print(query)
		#connect to DB
		conn = psycopg2.connect(
    		host="localhost",
    		database="smartnewsapp",
    		user="postgres",
    		password="postgres")

		cursor = conn.cursor()
		cursor.execute(query)
		cursor.execute("commit")
		return title
		
