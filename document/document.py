import json
import os
import sqlite3
from datetime import datetime
from uuid import uuid4

from flask import Blueprint, render_template, request, redirect, url_for

from config import Config

document_bp = Blueprint("/document", __name__, template_folder="templates")


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

        structure = request.form["structure"]

        list_doc = []

        d = request.files.keys()

        for x in d:

            file = request.files[x]

            if file.filename != "":
                doc_name = f'{uuid4()}.{file.filename.split(".")[-1].lower()}'

                file.save(os.path.join("static", Config.UPLOAD_FOLDER, doc_name))

                list_doc.append(doc_name)

        with sqlite3.connect(Config.DATABASE_URI) as con:
            cur = con.cursor()
            cur.execute(
                "INSERT INTO document (login,time,title,subtitle,content_page,structure,files) VALUES  (?,?,?,?,?,?,?)",
                (login, time, title, subtitle, content_page, structure, json.dumps(list_doc)))

        with sqlite3.connect(Config.DATABASE_URI) as con:
            cur = con.cursor()
            cur.execute(f"""SELECT id FROM document  WHERE title='{title}';""")
            entity_id = cur.fetchone()[0]

            return redirect(url_for('.update', entity_id=entity_id), 302)

    with sqlite3.connect(Config.DATABASE_URI) as con:
        cur = con.cursor()
        cur.execute(f"""SELECT title FROM Structure WHERE structure='Раздел документов';""")
        list_structure = cur.fetchall()

    print(list_structure)

    return render_template("add_document.html", list_structure=list_structure)


@document_bp.route("/document/edit/<int:entity_id>", methods=["GET", "POST"])
def update(entity_id):
    with sqlite3.connect(Config.DATABASE_URI) as con:
        cur = con.cursor()
    cur.execute(f"""SELECT login,title,subtitle,content_page,structure,files FROM document WHERE id='{entity_id}';""")
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
                    f"""UPDATE document SET login='{login}', title='{title}',subtitle='{subtitle}',content_page='{content_page}',structure='{structure}' WHERE id='{entity_id}';""")

            return redirect(url_for('.update', entity_id=entity_id), 302)

        if request.form["submit"] == "Удалить":
            delete(entity_id)
            return redirect(url_for(".show"))

    with sqlite3.connect(Config.DATABASE_URI) as con:
        cur = con.cursor()
        cur.execute(f"""SELECT title FROM Structure  WHERE structure='Раздел документов';""")
        list_structure = cur.fetchall()

    return render_template("edit_document.html", query=query, list_structure=list_structure,
                           lst=json.loads(query[-1][-1]))



@document_bp.route("/document/delete/<int:entity_id>", methods=["POST"])
def delete(entity_id):
    if request.method == "POST":
        with sqlite3.connect(Config.DATABASE_URI) as con:
            cur = con.cursor()
            cur.execute(f"""DELETE FROM document WHERE id='{entity_id}';""")
