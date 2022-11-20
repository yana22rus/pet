from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token, create_refresh_token, set_refresh_cookies
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import set_access_cookies

app = Flask(__name__)

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
jwt = JWTManager(app)


# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]

        password = request.form["password"]

        if username != "test" or password != "test":
            return jsonify({"msg": "Bad username or password"}), 401

        access_token = create_access_token(identity=username)
        refresh_token = create_refresh_token(identity=username)

        resp = jsonify({'login': True})
        set_access_cookies(resp, access_token)
        set_refresh_cookies(resp, refresh_token)
        return access_token

    return render_template("login.html")


@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    username = get_jwt_identity()
    return jsonify({'hello': 'from {}'.format(username)}), 200

@app.route("/")
#@jwt_required()
def index():

    return render_template("base.html")

if __name__ == "__main__":
    app.run(debug=True)
