import sqlite3, datetime, random, itertools


def inside():
    conn = sqlite3.connect("football.db")
    conn.execute("DELETE FROM MATCH_FIXTURE")
    conn.commit()
    conn.close()


if __name__ == '__main__':
    inside()

