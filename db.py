import sqlite3
from getpass import getuser

path = f"/home/{getuser()}/pet.sqlite"

with sqlite3.connect(path) as con:
    cur = con.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS Article (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    login STRING NOT NULL,
    time  STRING NOT NULL,
    seo_title STRING,
    seo_description STRING,
    title STRING NOT NULL UNIQUE,
    subtitle STRING,
    content_page STRING,
    short_link STRING,
    img STRING,
    is_deleted INTEGER NOT NULL DEFAULT 0,
    tag_news STRING
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS Document (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    login STRING NOT NULL,
    time  STRING NOT NULL,
    seo_title STRING,
    seo_description STRING,
    title STRING NOT NULL UNIQUE,
    subtitle STRING,
    content_page STRING,
    short_link STRING,
    files STRING,
    is_deleted INTEGER NOT NULL DEFAULT 0
    )""")



