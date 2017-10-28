import sqlite3

conn = sqlite3.connect("football.db")
cursor = conn.execute("SELECT  * FROM TEAM where TEAM_NAME=?", ('Real Madrid',)).fetchone()
b = ["teamName", "teamLogo", "country",
     "squadPic",
     "founded",
     "homeGround",
     "teamCost",
     "teamOwner",
     "teamSponsor",
     "teamCoach",
     "teamWebsite",
     "teamAbout"]
print(dict(zip(b,cursor)))


conn.close()
