import unittest
from flask import Flask,url_for
from .. import app,db,mod_user,mod_blog
from ..mod_user.models import User,Blog,UserComment
from ..mod_blog.forms import UserCommentForm


class UserCommentTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		app.config.from_object('config.TestingConfig')
		cls.app = app.test_client()
		cls.app_context = app.test_request_context()
		cls.app_context.push()
		db.create_all()

	@classmethod 	
	def tearDownClass(cls):
		db.session.remove()
		db.drop_all()

	def create_new_user(self):
		new_user = User(name="testuser", username="testuser1", email="shrutihdemo@gmail.com", password="1234")
		return new_user

	def get_created_new_user(self):
		get_new_user = User.query.filter_by(email='shrutihdemo@gmail.com').first()
		return get_new_user

	def test_user_comment_form_valid(self):
		data = {
				"comment_msg" : "Testing comment messages"
			}
		user_commentform = UserCommentForm(data = data)
		self.assertTrue(user_commentform.validate(),True)

	def test_user_comment_form_invalid(self):
		user_commentform = UserCommentForm(data = dict())
		self.assertFalse(user_commentform.validate(),False)

	def test_view_user_comment(self):
		new_user = create_new_user
		db.session.add(new_user)
		db.session.commit()
		email="shrutihdemo@gmail.com"
		password="1234"
		response = self.app.post('/login', data=dict(
				email=email,
				password=password
			), follow_redirects=True)

		blog =Blog(title="blog user comment test",description="We are testing user comments for blog",user_id=new_user.id)
		db.session.add(blog)
		db.session.commit()

		response = self.app.post(url_for('auth.blog_track',
									id=int(blog.id)
								),
							data=dict(
								content="This is user comments for blog"
								),
							follow_redirects=True)
		assert "User comments for blog" in response.data


	def test_reply_to_view_user_comment(self):
		new_user = create_new_user
		db.session.add(new_user)
		db.session.commit()
		email="shrutihdemo@gmail.com"
		password="1234"
		response = self.app.post('/login', data=dict(
				email=email,
				password=password
			), follow_redirects=True)

		blog =Blog(title="blog user comment test",description="We are testing user comments for blog",user_id=new_user.id)
		db.session.add(blog)
		db.session.commit()
		user_comment = UserComment.query.filter_by(content="This is user comments for blog").first()
		response = self.app.post(url_for('auth.blog_track',
									id=int(blog.id)
								),
							data=dict(
								content="Reply for blog user comment",
								parent_id = user_comment.id	
								),
							follow_redirects=True)