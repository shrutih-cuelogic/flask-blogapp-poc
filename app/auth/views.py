from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from flask_login import login_user , logout_user , current_user , login_required
from app.auth.forms import RegisterForm, ProfileEditForm, LoginForm
from app.blog.forms import UserCommentForm
from urllib2 import HTTPError
import json
from datetime import datetime
from . import auth
from .. import db
from models import User
from app.blog.models import Blog, UserComment
from requests_oauthlib import OAuth2Session
from config import Auth


def get_google_auth(state=None, token=None):
    if token:
        return OAuth2Session(Auth.CLIENT_ID, token=token)
    if state:
        return OAuth2Session(
            Auth.CLIENT_ID,
            state=state,
            redirect_uri=Auth.REDIRECT_URI)
    oauth = OAuth2Session(
        Auth.CLIENT_ID,
        redirect_uri=Auth.REDIRECT_URI,
        scope=Auth.SCOPE)
    return oauth

# Index
@auth.route('/')
def index():
    blogs = Blog.query.order_by(Blog.blog_updated_on.desc()).all()
    blogs_list = []
    if blogs:
        for blog in blogs:
            blog_dict = {
                'id' : blog.id,
                'user_id' : blog.user_id,
                'title' : blog.title,
                'description' : blog.description,
                'blog_created_on' : str(blog.blog_created_on),
                'blog_updated_on' : str(blog.blog_updated_on)
            }
            blogs_list.append(blog_dict)
    else:
        flash('There are no blogs yet')

    return render_template('index.html', blogs_list=blogs_list)

# View Full Blog
@auth.route('/blog_track/<blog_id>', methods=['GET', 'POST'])
def blog_track(blog_id):

    blogs = Blog.query.filter_by(id=blog_id).first()
    blog_comments = blogs.user_comments.all()
    blogs_list = []
    form = UserCommentForm()

    if form.validate_on_submit():
        if form.parent_comment_id.data == "":
            user_comment = UserComment(content=form.content.data, 
                blog=blogs.id, 
                user_id=current_user.id
                )
            db.session.add(user_comment)
            db.session.commit()
            blog_comments = blogs.user_comments.all()
        else:
            user_comment = UserComment(content=form.content.data, 
                blog=blogs.id, 
                user_id=current_user.id, 
                parent_comment_id=int(form.parent_comment_id.data)
            )
            db.session.add(user_comment)
            db.session.commit()
            blog_comments = blogs.user_comments.all()
        return redirect(url_for('auth.blog_track',blog_id=blogs.id))
    return render_template('auth/view_all_blogs.html', 
        blogs=blogs, 
        blog_comments=blog_comments,
        form=form)

# User Register
@auth.route('/register', methods=['GET', 'POST'])
def register():
    registerform = RegisterForm()
    if registerform.validate_on_submit():
        import pdb; pdb.set_trace();
        user_obj = User(name = registerform.name.data, 
            email = registerform.email.data, 
            username = registerform.username.data, 
            password = registerform.password.data,
            address = registerform.address.data
            )
        db.session.add(user_obj)
        db.session.commit()

        flash('You are now registered and can log in', 'success')

        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=registerform)

# Login
@auth.route('/login',methods=['GET','POST'])
def login():
    try:
        loginform = LoginForm()
        if current_user.is_authenticated:
            return redirect(url_for('.index'))

        google = get_google_auth()
        auth_url, state = google.authorization_url(
                                Auth.AUTH_URI, access_type='offline')
        session['oauth_state'] = state
        global oauth_state
        oauth_state = state

        if loginform.validate_on_submit():
            user = User.query.filter_by(email=loginform.email.data).first()
            if user is not None and user.verify_password(loginform.password.data):
                session['remember_me']=loginform.remember_me.data
                login_user(user,loginform.remember_me.data)
                return redirect(url_for('.index'))
            flash("Invalid Username and Password")  
        return render_template('auth/login.html', 
            form=loginform, 
            auth_url=auth_url
            )

    except Exception as e:
        return render_template('error.html', error = str(e))

@auth.route('/showProfile/<username>',methods=['GET','POST'])
@login_required
def view_profile(username):

    profile_editform = ProfileEditForm()
    if profile_editform.validate_on_submit():
        user_obj = User.query.filter_by(email=current_user.email).first()
        user_obj.username = profile_editform.username.data
        user_obj.email = profile_editform.email.data
        user_obj.address = profile_editform.address.data
        user_obj.contact = profile_editform.contact.data
        user_obj.gender = profile_editform.gender.data
        db.session.commit()
        flash('User profile update successfully.')
        return redirect(url_for('auth.view_profile',username=current_user))

    else:
        profile_editform.username.data = current_user.username
        profile_editform.email.data = current_user.email
        profile_editform.contact.data = current_user.contact
        profile_editform.address.data = current_user.address
        profile_editform.gender.data = current_user.gender

    return render_template('auth/view_profile.html',form=profile_editform)

@auth.route('/logout')
@login_required
def logout():
    """
    Handle requests to the /logout route
    Log an employee out through the logout link
    """
    logout_user()
    flash('You have successfully been logged out.')

    # redirect to the login page
    return redirect(url_for('.index'))

@auth.route('/oauth2callback')
def callback():
    # Redirect user to home page if already logged in.
    if current_user is not None and current_user.is_authenticated:
        return redirect(url_for('.index'))
    if 'error' in request.args:
        if request.args.get('error') == 'access_denied':
            return 'You denied access.'
        return 'Error encountered.'
    if 'code' not in request.args and 'state' not in request.args:
        return redirect(url_for('auth.login'))
    else:
        # Execution reaches here when user has
        # successfully authenticated our app.
        global oauth_state
        google = get_google_auth(state=oauth_state)
        try:
            token = google.fetch_token(
                Auth.TOKEN_URI,
                client_secret=Auth.CLIENT_SECRET,
                authorization_response=request.url)
        except HTTPError:
            return 'HTTPError occurred.'
        google = get_google_auth(token=token)
        resp = google.get(Auth.USER_INFO)
        if resp.status_code == 200:
            user_data = resp.json()
            email = user_data['email']
            user = User.query.filter_by(email=email).first()
            if user is None:
                user = User()
                user.email = email
            user.name = user_data['name']
            user.username = user_data['name']
            print(token)
            user.tokens = json.dumps(token)
            user.avatar = user_data['picture']
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('.index'))
        return 'Could not fetch your information.'

if __name__ == '__main__':
    app.run(debug=True)