from __future__ import unicode_literals
from django.db import models
from ..user_app.models import User

class PostManager(models.Manager):
	def post(self, user_board, poster, post):
		if len(post) < 1:
			return False
		else:
			Post.postManager.create(user_board_id=user_board, poster_id=poster, post=post)
			return True

class CommentManager(models.Manager):
	def comment(self, post, poster, comment):
		if len(comment) < 1:
			return False
		else:
			Comment.commentManager.create(post_id=post, poster_id=poster, comment=comment)
			return True

class Post(models.Model):
	user_board = models.ForeignKey(User, related_name="board")
	poster = models.ForeignKey(User)
	post = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	postManager = PostManager()

	def __repr__(self):
		return "<Post object: {} {} {}>".format(self.user_board.username, self.poster.username, self.post)

class Comment(models.Model):
	post = models.ForeignKey(Post, related_name="comments")
	poster = models.ForeignKey(User)
	comment = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	commentManager = CommentManager()
	
	def __repr__(self):
		return "<Comment object: {} {}>".format(self.poster.username, self.comment)
