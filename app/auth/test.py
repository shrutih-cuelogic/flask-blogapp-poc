import unittest
from flask import Flask,url_for
from . import app,db,auth
from app.blog import blog_mod
from ..auth.models import User
from ..blog.models import Blog
from ..auth.forms import RegisterForm
from flask_fixtures import FixturesMixin
from app.auth.auth_factory import UserFactory


class TestCase(unittest.TestCase, FixturesMixin):
	fixtures = ['auth_users.json']

	@classmethod
	def setUpClass(cls):
		app.config.from_object('config.TestConfig')
		cls.app = app.test_client()
		cls.app_context = app.test_request_context()
		cls.app_context.push()
		# db.create_all();
		UserFactory.create();

	@classmethod
	def tearDownClass(cls):
	 	db.session.remove()
		db.drop_all()

	def test_index_url(self):
		response = self.app.get('/')
		self.assertTrue(response.status_code,200)

	def test_register_url(self):
		response = self.app.get('/register')
		self.assertTrue(response.status_code,200)

	def test_login_url(self):
		response = self.app.get('/login')
		self.assertTrue(response.status_code,200)

	def test_logout_url(self):
		response = self.app.get('/logout')
		self.assertTrue(response.status_code,200)

	def test_view_profile_url(self):
		response = self.app.get('/showProfile')
		self.assertTrue(response.status_code,200)
	
	def test_register_form_invalid(self):
		data = { 'name' : 'testname',
		'email' : 'shrutihdemo@gmail.com'
		}
		register_form = RegisterForm(data = data)
		register_form.validate()
		self.assertEqual(register_form.validate(),False)

	def test_register_form_valid(self):
		data = { 'name' : 'testname',
		'username' : 'shrutih',
		'email' : 'shrutihdemo@gmail.com',
		'password': '123',
		'confirm' : '123',
		}
		register_form = RegisterForm(data = data)
		register_form.validate()
		self.assertEqual(register_form.validate(),True)

	def test_register_user_valid_msg(self):
		data = { 'name' : 'testname',
		'username' : 'shrutih',
		'email' : 'shrutihdemo@gmail.com',
		'password': '123',
		'confirm' : '123',
		}
		response = self.app.post('/register', 
			data=data, 
			follow_redirects=True
		)
		print response.data
		assert "You are now registered and can log in" in response.data

	def test_user_profile_form_invalid(self):
		data = { 'name' : 'testname',
		'email' : 'shrutihdemo@gmail.com',
		'username': '',
		}
		user_profile = ProfileEditForm(data = data)
		user_profile.validate()
		self.assertEqual(user_profile.validate(),False)

	def test_user_profile_form_valid(self):
		data = { 'name' : 'testname',
		'username' : 'shrutih',
		'email' : 'shrutihdemo@gmail.com',
		'password': '1234',
		'address': 'Chandni chowk, Nagpur',
		'contact': '87742688864',
		'gender' : 'Female'
		}
		user_profile = ProfileEditForm(data = data)
		user_profile.validate()
		self.assertEqual(user_profile.validate(),True)

	def test_login_valid(self):
		email="shrutihdemo@gmail.com"
		password="1234"
		response = self.app.post('/login', data=dict(
				email=email,
				password=password
			), follow_redirects=True)
		assert "Hi, test successfull" in response.data

	def test_logout(self):
		email="shrutihdemo@gmail.com"
		password="1234"
		response = self.app.post('/login', data=dict(
				email=email,
				password=password
			), follow_redirects=True)
		response = self.app.get('/logout', 
						follow_redirects=True)
		assert "You have been logged out" in response.data


	def test_login_invalid(self):
		email="shruti@gmail.com"
		password="1234"
		response = self.app.post('/login', data=dict(
				email=email,
				password=password
			), follow_redirects=True)
		assert "Invalid Username and Password" in response.data

