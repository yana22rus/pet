import os
import sqlite3
from datetime import datetime
from uuid import uuid4

from flask import Blueprint, render_template, request, redirect, url_for

from config import Config

document_bp = Blueprint("/q", __name__, template_folder="templates")



@document_bp.route("/document", methods=["GET", "POST"])
def show():
    with sqlite3.connect(Config.DATABASE_URI) as con:
        cur = con.cursor()
        cur.execute(f"""SELECT id,title,subtitle,login,time FROM document;""")
        data = cur.fetchall()

    if request.method == "POST":
        delete(request.form["delete"])

        return redirect(url_for(".show"))

    return render_template("document.html", data=data)


@document_bp.route("/document/add", methods=["GET", "POST"])
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
            cur.execute("INSERT INTO document (login,time,title,subtitle,content_page,img) VALUES  (?,?,?,?,?,?)",
                        (login, time, title, subtitle, content_page, img))

        with sqlite3.connect(Config.DATABASE_URI) as con:
            cur = con.cursor()
            cur.execute(f"""SELECT id FROM document  WHERE title='{title}';""")
            news_id = cur.fetchone()[0]

            return redirect(url_for('.update', news_id=news_id), 302)

    return render_template("document_add.html")


@document_bp.route("/document/edit/<int:news_id>", methods=["GET", "POST"])
def update(news_id):
    with sqlite3.connect(Config.DATABASE_URI) as con:
        cur = con.cursor()
    cur.execute(f"""SELECT login,title,subtitle,content_page,img FROM document  WHERE id='{news_id}';""")
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
                    f"""UPDATE document SET login='{login}', title='{title}',subtitle='{subtitle}',content_page='{content_page}' WHERE id='{news_id}';""")

            return redirect(url_for('.update', news_id=news_id), 302)

        if request.form["submit"] == "Удалить":
            delete(news_id)
            return redirect(url_for(".show"))

    return render_template("edit_document.html", query=query)


@document_bp.route("/document/delete/<int:news_id>", methods=["POST"])
def delete(news_id):
    if request.method == "POST":
        with sqlite3.connect(Config.DATABASE_URI) as con:
            cur = con.cursor()
            cur.execute(f"""DELETE FROM document WHERE id='{news_id}';""")
