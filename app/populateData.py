import sqlite3, datetime, random, itertools


def inside():
    conn = sqlite3.connect("football.db")
    cursor = conn.execute("SELECT MATCH_DATE , TEAM1 , TEAM2 , LOCATION , STADIUM   FROM MATCH_FIXTURE ,MATCH_VENUE")
    for x in cursor:
        print(x)
    conn.commit()
    conn.close()



if __name__ == '__main__':
    inside()

