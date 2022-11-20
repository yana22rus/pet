from flask import Flask
from flask_jwt_extended import JWTManager
from config import Config
app = Flask(__name__)
app.config.from_object(Config)

jwt = JWTManager(app)

side_bar = [{"name": "Новости", "url": "/article"}, {"name": "Документы", "url": "/document"},
            {"name": "Опрос", "url": "/survey"},
            {"name": "Викторина", "url": "/quiz"},
            {"name": "Структура", "url": "/structure"}, {"name": "Теги новостей", "url": "/tag_new"},
            {"name": "Теги документов", "url": "/tag_document"}, {"name": "Фоторепортажи", "url": "/photo_report"},
            {"name": "Видео репортажи", "url": "/video_report"}
            ]

footer = [{"name": "Администрирование", "url": "/admin"}, {"name": " Центральный сайт ", "url": "/main"},
          {"name": "Дочерний сайт", "url": "/subsites"}]

from article.article import article_bp

app.register_blueprint(article_bp)
app.jinja_env.globals.update(side_bar=side_bar)
app.jinja_env.globals.update(footer=footer)

app.run(debug=True)

# # Create a route to authenticate your users and return JWTs. The
# # create_access_token() function is used to actually generate the JWT.
# @app.route("/login", methods=["GET", "POST"])
# def login():
#     if request.method == "POST":
#         username = request.form["username"]
#
#         password = request.form["password"]
#
#         if username != "test" or password != "test":
#             return jsonify({"msg": "Bad username or password"}), 401
#
#         access_token = create_access_token(identity=username)
#         refresh_token = create_refresh_token(identity=username)
#
#         resp = jsonify({'login': True})
#         set_access_cookies(resp, access_token)
#         set_refresh_cookies(resp, refresh_token)
#         return access_token
#
#     return render_template("login.html")
#
#
# @app.route("/protected", methods=["GET"])
# @jwt_required()
# def protected():
#     # Access the identity of the current user with get_jwt_identity
#     username = get_jwt_identity()
#     return jsonify({'hello': 'from {}'.format(username)}), 200
#
#
# @app.route("/")
# # @jwt_required()
# def index():
#     return render_template("base.html")
