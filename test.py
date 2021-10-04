#!/usr/bin/python

import sqlite3

conn = sqlite3.connect('db')
conn.execute("drop table newsapp_user")
