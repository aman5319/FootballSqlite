import sqlite3, datetime, random, itertools
import tabulate
from prettytable import PrettyTable


def inside():
    conn = sqlite3.connect("football.db")
    cursor = conn.execute("SELECT PLAYER_NAME , JERSEY_NUMBER FROM PLAYER WHERE JERSEY_NUMBER=7").fetchall()
    conn.commit()
    conn.close()
    return cursor



if __name__ == '__main__':
    print(inside())

