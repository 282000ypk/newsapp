from flask_login import UserMixin

from db import get_db

class User(UserMixin):
	def __init__(self, id_, name, email, profile_pic_url):
		self.id = id_
		self.name = name
		self.email = email
		self.profile_pic_url = profile_pic_url

	@staticmethod
	def get(user_id):
		db = get_db()
		print(db)
		user = db.execute("select * from newsapp_user where id= ?", (user_id,)).fetchone()

		if not user:
			return None

		user = User(id = user[0],name = user[1], email = user[2], profile_pic_url = user[3])

		return user

	@staticmethod
	def create(id_, name, email, profile_pic_url):
		db = get_db()
		print(db)
		db.execute("insert into newsapp_user (id, name, email, profile_pic_url) values(?, ?, ?, ?)",(id_, name, email, profile_pic_url,))
		db.commit()






