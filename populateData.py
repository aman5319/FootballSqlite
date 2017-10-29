import sqlite3

conn = sqlite3.connect("football.db")
cursor = conn.execute("SELECT  TEAM_NAME FROM TEAM ")
b = ["teamName"]
list1=[]
for line in cursor:
     list1.append(dict(zip(b,line)))

print(list1)

conn.close()
