from flask import jsonify, request, g, url_for, current_app
from .. import db
from . import api
from ..models import Post, Permission, Comment
from .decorators import permission_required

@api.route('/comments/')
def get_comments():
  page = request.args.get('page', 1, type=int)
  pagination = Comment.query.order_by(Comment.timestamp.desc()).paginate(
      page,  per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
      error_out = False
    )
  comments = pagination.items
  prev = None
  if pagination.has_prev:
    prev = url_for('api.get_comments', page = page - 1, _external = True)

  next = None
  if pagination.has_next:
    next = url_for('api.get_comments', page = page + 1, _external = True)

  return jsonify({
    'comments': [comment.to_json() for comment in comments],
    'prev': prev,
    'next': next,
    'count': pagination.total
  })

@api.route('/posts/<int:id>/comments/', methods=['POST'])
@permission_required(Permission.COMMENT)
def new_post_comment(id):
    post = Post.query.get_or_404(id)
    comment = Comment.from_json(request.json)
    comment.author = g.current_user
    comment.post = post
    db.session.add(comment)
    db.session.commit()
    return jsonify(comment.to_json()), 201, \
        {'Location': url_for('api.get_comments', id=comment.id,
                             _external=True)}
