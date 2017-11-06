import sqlite3, datetime, random, itertools
import tabulate
from prettytable import PrettyTable


def inside():
    conn = sqlite3.connect("football.db")
    cursor = conn.execute("SELECT  datetime('now')").fetchone()
    conn.commit()
    conn.close()
    return cursor



if __name__ == '__main__':
    print(inside()[0])
