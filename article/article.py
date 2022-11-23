import os
import sqlite3
from datetime import datetime
from uuid import uuid4

from flask import Blueprint, render_template, request, redirect, url_for

from config import Config

article_bp = Blueprint("/", __name__, template_folder="templates")

@article_bp.route("/")
def index():
    return ""


@article_bp.route("/article", methods=["GET", "POST"])
def article():

    with sqlite3.connect(Config.DATABASE_URI) as con:
        cur = con.cursor()
        cur.execute(f"""SELECT id,title,subtitle,login,time FROM Article;""")
        data = cur.fetchall()


    return render_template("article.html",data=data)


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

    if request.method == "POST":

        if request.form["submit"] == "Сохранить":

            login = "test"

            title = request.form["title"]

            subtitle = request.form["subtitle"]

            content_page = request.form["content_page"]

            with sqlite3.connect(Config.DATABASE_URI) as con:
                cur = con.cursor()
                cur.execute(
                    f"""UPDATE Article SET login='{login}', title='{title}',subtitle='{subtitle}',content_page='{content_page}' WHERE id='{news_id}';""")

            return redirect(url_for('.update', news_id=news_id), 302)

        if request.form["submit"] == "Удалить":
            delete(news_id)
            return redirect(url_for(".index"))

    return render_template("edit_article.html", query=query)


@article_bp.route("/article/delete/<int:news_id>", methods=["POST"])
def delete(news_id):
    if request.method == "POST":
        with sqlite3.connect(Config.DATABASE_URI) as con:
            cur = con.cursor()
            cur.execute(f"""DELETE FROM Article WHERE id='{news_id}';""")
