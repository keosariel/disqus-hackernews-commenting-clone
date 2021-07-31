from flask import Blueprint, request, current_app, render_template, abort
from app.models import Post
from app.utils import get_author, json_response, render_post
from app import basedir
import os

post = Blueprint("post", __name__, template_folder=os.path.join(basedir, "templates"))


@post.route("/")
def get_post():
	url = request.args.get("url")

	if url:
		post = Post.query.filter_by(content=url, parent_id=0).first()
		author = get_author(request.remote_addr)
		if not post:
			post = Post(
				content=url,
				parent_id=0,
				author_id=author.id
			)

			post.save()

		return render_template("index.html", post=post, current_author=author, render_post=render_post)

	return abort(404)

@post.route("/posts", methods=["POST"])
def add_post():
	json_data = request.json

	with current_app.app_context():
		author  = get_author(request.remote_addr)
		content = json_data.get("content").strip()
		parent_id = int(json_data.get("parent_id"))
		depth = int(json_data.get("depth"))

		if content:
			post = Post(
				content=content,
				parent_id=parent_id,
				author_id=author.id
			)

			post.save()
			

			return json_response(render_post(post, author, depth=depth), status=200)

	return json_response(None, has_error=True, description="Error adding post!", status=401)

@post.route("/posts/<int:post_id>", methods=["DELETE"])
def delete_post(post_id):
	json_data = request.json

	with current_app.app_context():
		author = get_author(request.remote_addr)

		post = Post.query.get(post_id)
		if post:
			if post.author == author:
				post_votes = Vote.query.filter_by(post_id=post_id).all()
				for  v in post_votes:
					v.delete()
				post.delete()
				return json_response(None, status=200)

	return json_response(None, has_error=True, description="Error deleting post!", status=401)
