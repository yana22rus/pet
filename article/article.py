import os
import sqlite3
from datetime import datetime
from uuid import uuid4

from flask import Blueprint, render_template, request, redirect, url_for

from config import Config

article_bp = Blueprint("/article", __name__, template_folder="templates")


@article_bp.route("/article", methods=["GET", "POST"])
def show():
    with sqlite3.connect(Config.DATABASE_URI) as con:
        cur = con.cursor()
        cur.execute(f"""SELECT id,title,subtitle,login,time FROM Article;""")
        data = cur.fetchall()

    if request.method == "POST":
        delete(request.form["delete"])

        return redirect(url_for(".show"))

    return render_template("structure.html", data=data)


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

        structure = request.form["structure"]

        file.save(os.path.join("static", Config.UPLOAD_FOLDER, img))

        with sqlite3.connect(Config.DATABASE_URI) as con:
            cur = con.cursor()
            cur.execute(
                "INSERT INTO Article (login,time,title,subtitle,content_page,img,structure) VALUES  (?,?,?,?,?,?,?)",
                (login, time, title, subtitle, content_page, img, structure))

        with sqlite3.connect(Config.DATABASE_URI) as con:
            cur = con.cursor()
            cur.execute(f"""SELECT id FROM Article  WHERE title='{title}';""")
            entity_id = cur.fetchone()[0]

            return redirect(url_for('.update', entity_id=entity_id), 302)

    with sqlite3.connect(Config.DATABASE_URI) as con:
        cur = con.cursor()
        cur.execute(f"""SELECT title FROM Structure  WHERE structure='Раздел новостей';""")
        list_structure = cur.fetchall()

    print(list_structure)

    return render_template("add_article.html", list_structure=list_structure)


@article_bp.route("/article/edit/<int:entity_id>", methods=["GET", "POST"])
def update(entity_id):
    with sqlite3.connect(Config.DATABASE_URI) as con:
        cur = con.cursor()
    cur.execute(f"""SELECT login,title,subtitle,content_page,img,structure FROM Article  WHERE id='{entity_id}';""")
    query = [cur.fetchone()]

    with sqlite3.connect(Config.DATABASE_URI) as con:
        cur = con.cursor()
        cur.execute(f"""SELECT title FROM Structure  WHERE structure='Раздел новостей';""")
        list_structure = cur.fetchall()

    if request.method == "POST":

        if request.form["submit"] == "Сохранить":
            login = "test"

            title = request.form["title"]

            subtitle = request.form["subtitle"]

            content_page = request.form["content_page"]

            structure = request.form["structure"]

            with sqlite3.connect(Config.DATABASE_URI) as con:
                cur = con.cursor()
                cur.execute(
                    f"""UPDATE Article SET login='{login}', title='{title}',subtitle='{subtitle}',content_page='{content_page}',structure='{structure}' WHERE id='{entity_id}';""")

            return redirect(url_for('.update', entity_id=entity_id), 302)

        if request.form["submit"] == "Удалить":
            delete(entity_id)
            return redirect(url_for(".show"))


    return render_template("edit_article.html", query=query, list_structure=list_structure)


@article_bp.route("/article/delete/<int:entity_id>", methods=["POST"])
def delete(entity_id):
    if request.method == "POST":
        with sqlite3.connect(Config.DATABASE_URI) as con:
            cur = con.cursor()
            cur.execute(f"""DELETE FROM Article WHERE id='{entity_id}';""")
