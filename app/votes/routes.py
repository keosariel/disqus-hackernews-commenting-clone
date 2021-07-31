from flask import Blueprint, request, current_app
from app.models import Vote
from app.utils import get_author, json_response, render_post
vote = Blueprint("vote", __name__)

@vote.route("/votes/<int:post_id>", methods=["POST", "DELETE"])
def add_vote(post_id):

	with current_app.app_context():
		author = get_author(request.remote_addr)
		_vote = Vote.query.filter_by(post_id=post_id, author_id=author.id).first()

		if request.method == "POST":
			if not _vote:
				vote = Vote(
					value=1,
					post_id=post_id,
					author_id=author.id
				)

				vote.save()
		elif request.method == "DELETE":
			if _vote:
				_vote.delete()

		return json_response(None, status=200)

	return json_response(None, has_error=True, description="Error adding vote!", status=401)
