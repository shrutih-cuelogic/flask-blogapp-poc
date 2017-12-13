from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from flask_login import current_user , login_required
# from passlib.hash import sha256_crypt
# from functools import wraps
import json
import re
from datetime import datetime
from . import blog_mod
from .. import db
from models import Blog


@blog_mod.route('/blogHome')
@login_required
def blog_home():
    return render_template('blog/blog_home.html')

@blog_mod.route('/showAddBlog')
@login_required
def show_add_blog():
    return render_template('blog/add_blog.html')

@blog_mod.route('/addBlog',methods=['POST'])
@login_required
def add_blog():
    if current_user:
        if request.form['inputTitle'] and request.form['inputDescription']:
            blog_desc = re.sub('<[^>]*>', '', request.form['inputDescription'])
            blog_obj = Blog(title = request.form['inputTitle'], 
                description = blog_desc,
                user_id = current_user.id
                )
            db.session.add(blog_obj)
            if blog_obj:
                db.session.commit()
                flash('You have successfully created your blog', 'success')
                return redirect(url_for('blog_mod.blog_home'))
            else:
                return render_template('error.html',error = 'No data found')
        else:
            flash('Please enter blog details' , 'error')

@blog_mod.route('/getBlog')
@login_required
def get_currentuser_blog():
    try:
        if current_user:
            blogs = current_user.blogs.order_by(Blog.blog_updated_on.desc()).all()
            if blogs:
                blogs_list = []
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

                return json.dumps(blogs_list)
            else:
                return render_template('error.html', error = 'Current user has no blogs')
        else:
            return render_template('error.html', error = 'Unauthorized Access')
    except Exception as e:
        return render_template('error.html', error = str(e))

@blog_mod.route('/getBlogById',methods=['POST'])
def get_blog_by_id():
    try:
        if current_user:
            blog_id = request.form['id']
            blogs = Blog.query.filter_by(id = blog_id, 
                user_id = current_user.id
                ).first()
 
            blog = []
            blog.append({'id':blogs.id, 
                'title':blogs.title, 
                'description':blogs.description})
 
            return json.dumps(blog)
        else:
            return render_template('error.html', error = 'Unauthorized Access')
    except Exception as e:
        return render_template('error.html',error = str(e))

@blog_mod.route('/updateBlog', methods=['POST'])
def update_blog():
    try:
        if current_user:
            blog_id = request.form['id']
            blog = Blog.query.filter_by(id=blog_id).first()
            blog.title = request.form['title']
            blog.description = request.form['description']
            if blog:
                db.session.commit()
                flash('Blog Updated Successfully')
                return json.dumps({'status':'OK'})
            else:
                return json.dumps({'status':'ERROR'})
    except Exception as e:
        return json.dumps({'status':'Unauthorized access'})

@blog_mod.route('/deleteBlog', methods=['POST'])
def delete_blog():
    try:
        if current_user:
            blog_id = request.form['id']
            blog = Blog.query.filter_by(id=blog_id, user_id=current_user.id).delete()
            if blog is not None:
                db.session.commit()
                flash('Blog Deleted Successfully')
                return json.dumps({'status':'OK'})
            else:
                return json.dumps({'status':'ERROR'})
        else:
            return render_template('error.html',error = 'Unauthorized Access')
    except Exception as e:
        return json.dumps({'status':str(e)})