from flask import jsonify, render_template
from app.models import Author

def render_post(post, current_author, depth):
	return render_template("post.html", 
							post=post, 
							render_post=render_post, 
							current_author=current_author, 
							depth=depth)

def get_author(ip_addr):
	"""Add author if author doesn't exists"""
	author = Author.query.filter_by(ip_address=ip_addr).first()
	if not author:
		author = Author(ip_address=ip_addr)
		author.save()

	return author

def json_response(data, has_error=False, description=None, status=200):

	return jsonify(
		{
			"data"       : data,
			"has_error"  : has_error,
			"description": description,
			"status": status
		}
	), status