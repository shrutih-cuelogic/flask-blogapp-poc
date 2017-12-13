import unittest
from flask import Flask,url_for
from .. import app,db,auth
from app.blog import blog_mod
from ..blog.models import Blog
from ..auth.forms import RegisterForm
from app.blog.blog_factory import BlogFactory


class TestCase(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		app.config.from_object('config.TestConfig')
		cls.app = app.test_client()
		cls.app_context = app.test_request_context()
		cls.app_context.push()
		# db.create_all();
		BlogFactory.create();

	@classmethod
	def tearDownClass(cls):
	 	db.session.remove()
		BlogFactory.drop_all()

	def test_index_url(self):
		response = self.app.get('/')
		self.assertTrue(response.status_code,200)

	def test_addblog_url(self):
		response = self.app.get('/addBlog')
		self.assertTrue(response.status_code,401)

	def test_getblog_url(self):
		response = self.app.get('/getBlog')
		self.assertTrue(response.status_code,200)

	def test_getblogby_id_url(self):
		response = self.app.get('/getBlogById')
		self.assertTrue(response.status_code,200)

	def test_updateblog_url(self):
		response = self.app.get('/updateBlog')
		self.assertTrue(response.status_code,200)

	def test_deleteblog_url(self):
		response = self.app.get('/deleteBlog')
		self.assertTrue(response.status_code,200)

	def test_addblog_valid_msg(self):
		data = { 'title' : 'Blog11',
		'description' : 'this is blog111 test'
		}
		response = self.app.post('/addBlog', 
			data=data, 
			follow_redirects=True
		)
		print response.data
		assert "You have successfully created your blog" in response.data

	def test_updateblog_valid_msg(self):
		data = { 'title' : 'Blog11test234',
		'description' : 'this is blog111 test'
		}
		response = self.app.post('/updateBlog', 
			data=data, 
			follow_redirects=True
		)
		print response.data
		assert "Blog Updated Successfully" in response.data

	def test_addblog_valid_msg(self):
		data = { 'title' : 'Blog11',
		'description' : 'this is blog111 test'
		}
		response = self.app.post('/deleteBlog', 
			data=data, 
			follow_redirects=True
		)
		print response.data
		assert "Blog Deleted Successfully" in response.data