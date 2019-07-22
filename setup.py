import sqlite3

conn = sqlite3.connect('email.db')
cursor = conn.cursor()

cursor.execute("CREATE TABLE users (userId uuid, address string);")
cursor.execute("CREATE TABLE mail (id uuid, recipient uuid, sender String, message String, archived Boolean)")

conn.commit()