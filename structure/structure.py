import sqlite3
from datetime import datetime

from flask import Blueprint, render_template, request, redirect, url_for

from config import Config

structure_bp = Blueprint("/structure", __name__, template_folder="templates")

default_value_structure = ("Простой раздел",
    "Раздел новостей", "Раздел документов", "Раздел опросов", "Раздел викторин", "Раздел фоторепортажей",
    "Раздел видео-репортажей")


@structure_bp.route("/structure", methods=["GET", "POST"])
def show():
    with sqlite3.connect(Config.DATABASE_URI) as con:
        cur = con.cursor()
        cur.execute(f"""SELECT id,title,subtitle,login,time FROM structure;""")
        data = cur.fetchall()

    if request.method == "POST":
        delete(request.form["delete"])

        return redirect(url_for(".show"))

    return render_template("structure.html", data=data)


@structure_bp.route("/structure/add", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        login = "admin"

        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        title = request.form["title"]

        subtitle = request.form["subtitle"]

        content_page = request.form["content_page"]

        structure = request.form["structure"]

        with sqlite3.connect(Config.DATABASE_URI) as con:
            cur = con.cursor()
            cur.execute("INSERT INTO structure (login,time,title,subtitle,content_page,structure) VALUES  (?,?,?,?,?,?)",
                        (login, time, title, subtitle, content_page,structure))

        with sqlite3.connect(Config.DATABASE_URI) as con:
            cur = con.cursor()
            cur.execute(f"""SELECT id FROM structure WHERE title='{title}';""")
            entity_id = cur.fetchone()[0]

            return redirect(url_for('.update', entity_id=entity_id), 302)

    return render_template("add_structure.html",default_value_structure=default_value_structure)


@structure_bp.route("/structure/edit/<int:entity_id>", methods=["GET", "POST"])
def update(entity_id):
    with sqlite3.connect(Config.DATABASE_URI) as con:
        cur = con.cursor()
    cur.execute(f"""SELECT login,title,subtitle,content_page,structure FROM structure  WHERE id='{entity_id}';""")
    query = [cur.fetchone()]

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
                    f"""UPDATE structure SET login='{login}', title='{title}',subtitle='{subtitle}',content_page='{content_page}',structure='{structure}'  WHERE id='{entity_id}';""")

            return redirect(url_for('.update', entity_id=entity_id), 302)

        if request.form["submit"] == "Удалить":
            delete(entity_id)
            return redirect(url_for(".show"))

    return render_template("edit_structure.html", query=query,default_value_structure=default_value_structure)


@structure_bp.route("/structure/delete/<int:entity_id>", methods=["POST"])
def delete(entity_id):
    if request.method == "POST":
        with sqlite3.connect(Config.DATABASE_URI) as con:
            cur = con.cursor()
            cur.execute(f"""DELETE FROM structure WHERE id='{entity_id}';""")
