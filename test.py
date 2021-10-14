#!/usr/bin/python

import sqlite3

conn = sqlite3.connect('db')
#conn.execute("create table news(title text primary key, u_id text references newsapp_user(id), positive int, negative int)")


conn.execute("insert into news values('NASA Invites Media to James Webb Space Telescope Launch - India Education Diary', '115612343747350680365', 0, 1)")
rows = conn.execute("select * from news")

for i in rows:
	print(i)
