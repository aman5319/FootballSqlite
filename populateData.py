import sqlite3

conn = sqlite3.connect("football.db")
cursor = conn.execute("Drop TABLE FEEDBACK")
conn.commit()
conn.close()
