from flask import Blueprint, render_template, request
from app import basedir
import os
from app.models import Post, Vote, User

main = Blueprint("main", __name__, template_folder=os.path.join(basedir, "templates"))

@main.route("/", methods=["GET"])
@main.route("/home", methods=["GET"])
def home():
	token = request.cookies.get("uid")
	posts = Post.query.all()
	user  = None

	if token:
		valid, user_id = User.decode_token(token)
		if valid:
			user = User.query.get(user_id)

	return render_template("index.html", posts=posts, user=user)
