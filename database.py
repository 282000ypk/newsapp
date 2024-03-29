import psycopg2
import os

class Database():

	def __init__(self, conn):
		self.conn = conn
		
	@staticmethod
	def get_local_connection():
		conn = psycopg2.connect(
    		host="localhost",
    		database="smartnewsapp",
    		user="postgres",
    		password="postgres")
		return conn
	# conn = Database.get_local_connection()
	
	@staticmethod
	def get_server_connection():
		DBString = os.environ.get("DATABASE_URL")
		DBString = DBString[10:]
		username = DBString.split("@")[0].split(":")[0]
		password = DBString.split("@")[0].split(":")[1]
		host = DBString.split("@")[0].split(":")[0]
		host = DBString.split("@")[0].split("/")[1]
		conn = psycopg2.connect(
    		host="ec2-34-202-66-20.compute-1.amazonaws.com",
    		database="dciuebpcuvjmdm",
    		user="xydcdkhjxeamwm",
    		password="58022ff4cb2dae17c3eb06a36035c7725896f2b63907f819d51a4b7bc247db89")
		return conn
	# conn = Database.get_server_connection()
	

