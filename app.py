"""Blogly application."""

from flask import Flask, render_template, request, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///blogly"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "secrets"
app.config ['DEBUG_TB_INTERCEPT_REDIRECTS']= False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

"""Homepage"""
@app.route('/')
def root():
    return redirect("/user")

"""Show user page"""
@app.route('/user')
def list_users():
    user = User.query.all()
    return render_template('user.html', user=user)

"""Show add new user form"""
@app.route('/new_user', methods=["GET"])
def show_new_user_form():
    return render_template('new_user.html')

"""Add new user"""
@app.route('/new_user', methods=["POST"])
def add_new_user():
    new_user = User(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        image_url=request.form['image_url'] or None)

    db.session.add(new_user)
    db.session.commit()

    return redirect ('/user')

"""Show user detail page"""
@app.route('/user/<int:user_id>')
def show_user_details(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('detail.html', user=user)

"""Show User Edit form"""
@app.route('/user/<int:user_id>/edit', methods=["GET"])
def show_edit_form(user_id):
    user= User.query.get_or_404(user_id)
    return render_template('edit.html', user=user)

"""Submit User Edit Form"""
@app.route('/user/<int:user_id>/edit', methods=["POST"])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect("/user")

"""Delete User"""
@app.route('/user/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
   
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/user")

#POST ROUTE!
"""Show a new post form"""
@app.route('/user/<int:user_id>/new_post')
def show_new_post_form(user_id):
    user = User.query.get_or_404(user_id)
    tag = Tag.query.all()
    return render_template('new_post.html', user=user, tag=tag)

"""Add a new post"""
@app.route('/user/<int:user_id>/new_post', methods=["POST"])
def add_new_post(user_id):
    user = User.query.get_or_404(user_id)
    tag_ids = [int(num) for num in request.form.getlist("tag")]
    tag = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    new_post = Post(
        title=request.form['title'],
        content=request.form['content'], user=user, tag=tag)

    db.session.add(new_post)
    db.session.commit()

    return redirect(f"/user/{user_id}")

"""Show post"""
@app.route('/post/<int:post_id>')
def show_post_details(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post_detail.html', post=post)

"""Show edit post form"""
@app.route('/post/<int:post_id>/edit')
def show_edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    tag = Tag.query.all()
    
    return render_template('edit_post.html', post=post, tag=tag)

"""Submit edit post form"""
@app.route('/post/<int:post_id>/edit', methods=["POST"])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']
    tag_ids = [int(num) for num in request.form.getlist("tag")]
    post.tag = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    db.session.add(post)
    db.session.commit()
    user_id = post.user.id

    return redirect(f"/user/{user_id}")

"""Delete post"""
@app.route('/post/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
   
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()

    return redirect("/user")

#TAG ROUTE!
"""Show tags"""
@app.route('/tag')
def tag():
    tag = Tag.query.all()
    return render_template('tag.html', tag=tag)

"""Show new tag form"""
@app.route('/new_tag')
def new_tag_form():
    post = Post.query.all()
    return render_template('new_tag.html', post=post)

"""Submit new tag form"""
@app.route('/new_tag', methods=["POST"])
def new_tag():
    post_ids = [int(num) for num in request.form.getlist("post")]
    post = Post.query.filter(Post.id.in_(post_ids)).all()
    new_tag = Tag(name=request.form['name'], post=post)

    db.session.add(new_tag)
    db.session.commit()

    return redirect("/tag")

"""Show tag information"""
@app.route('/tag/<int:tag_id>')
def show_tag(tag_id):
    tag= Tag.query.get_or_404(tag_id)
    return render_template('show_tag.html', tag=tag)

"""Show edit tag form"""
@app.route('/tag/<int:tag_id>/edit')
def edit_tag_form(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    post = Post.query.all()
    return render_template('edit_tag.html', tag=tag, post=post)

"""Submit edit tag form"""
@app.route('/tag/<int:tag_id>/edit', methods=["POST"])
def edit_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']
    post_ids = [int(num) for num in request.form.getlist("post")]
    tag.post = Post.query.filter(Post.id.in_(post_ids)).all()

    db.session.add(tag)
    db.session.commit()

    return redirect("/tag")

"""Delete Tag"""
@app.route('/tag/<int:tag_id>/delete', methods=["POST"])
def delete_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()

    return redirect("/tag")



    

