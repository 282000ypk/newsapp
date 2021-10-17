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
		conn = psycopg2.connect(
    		host="localhost",
    		database="smartnewsapp",
    		user="postgres",
    		password="postgres")
		#user = db.execute("select * from newsapp_user where id= ?", (user_id,)).fetchone()

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

