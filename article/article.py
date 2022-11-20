import os
import sqlite3
from datetime import datetime
from uuid import uuid4

from flask import Blueprint, render_template, request, redirect, url_for

from config import Config

article_bp = Blueprint("/", __name__, template_folder="templates")


@article_bp.route("/article/add", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        login = "admin"

        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        title = request.form["title"]

        subtitle = request.form["subtitle"]

        content_page = request.form["content_page"]

        file = request.files["img"]

        img = f'{uuid4()}.{file.filename.split(".")[-1].lower()}'

        print(img)

        file.save(os.path.join("static", Config.UPLOAD_FOLDER, img))

        with sqlite3.connect(Config.DATABASE_URI) as con:
            cur = con.cursor()
            cur.execute("INSERT INTO Article (login,time,title,subtitle,content_page,img) VALUES  (?,?,?,?,?,?)",
                        (login, time, title, subtitle, content_page, img))

        with sqlite3.connect(Config.DATABASE_URI) as con:
            cur = con.cursor()
            cur.execute(f"""SELECT id FROM Article  WHERE title='{title}';""")
            news_id = cur.fetchone()[0]

            return redirect(url_for('.update', news_id=news_id), 302)

    return render_template("article_add.html")


@article_bp.route("/article/edit/<int:news_id>", methods=["GET", "POST"])
def update(news_id):
    with sqlite3.connect(Config.DATABASE_URI) as con:
        cur = con.cursor()
    cur.execute(f"""SELECT login,title,subtitle,content_page,img FROM Article  WHERE id='{news_id}';""")
    query = [cur.fetchone()]

    return render_template("edit_article.html", query=query)