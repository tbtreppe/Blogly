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

@app.route('/')
def root():
    return redirect("/user")

@app.route('/user')
def list_users():
    user = User.query.all()
    return render_template('user.html', user=user)

@app.route('/new_user', methods=["GET"])
def show_new_user_form():
    return render_template('new_user.html')

@app.route('/new_user', methods=["POST"])
def add_new_user():
    new_user = User(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        image_url=request.form['image_url'] or None)

    db.session.add(new_user)
    db.session.commit()

    return redirect ('/user')

@app.route('/user/<int:user_id>')
def show_user_details(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('detail.html', user=user)

@app.route('/user/<int:user_id>/edit', methods=["GET"])
def show_edit_form(user_id):
    user= User.query.get_or_404(user_id)
    return render_template('edit.html', user=user)

@app.route('/user/<int:user_id>/edit', methods=["POST"])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect("/user")

@app.route('/user/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
   
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/user")

#POST ROUTE!

@app.route('/user/<int:user_id>/new_post')
def show_new_post_form(user_id):
    user = User.query.get_or_404(user_id)
    tag = Tag.query.all()
    return render_template('new_post.html', user=user, tag=tag)

@app.route('/user/<int:user_id>/new_post', methods=["POST"])
def add_new_post(user_id):
    user = User.query.get_or_404(user_id)
    tag_id = [int(num) for num in request.form.getlist("tag")]
    tag = Tag.query.filter(Tag.id.in_(tag_id)).all()

    new_post = Post(
        title=request.form['title'],
        content=request.form['content'], user=user, tag=tag)

    db.session.add(new_post)
    db.session.commit()

    return redirect(f"/user/{user_id}")

@app.route('/post/<int:post_id>')
def show_post_details(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post_detail.html', post=post)

@app.route('/post/<int:post_id>/edit')
def show_edit_post(post_id):
    post = Post.query.get_or404(post_id)
    tag = Tag.query.all()
    
    return render_template('edit_post.html', post=post, tag=tag)

@app.route('/post/<int:post_id>/edit', methods=["POST"])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']
    tag_id = [int(num) for num in request.form.getlist("tag")]
    post.tag = Tag.query.filter(Tag.id.in_(tag_id)).all()

    db.session.add(post)
    db.session.commit()

    return redirect(f"/user/{post.user_id}")

@app.route('/post/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
   
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()

    return redirect("/user")

#TAG ROUTE!

@app.route('/tag')
def tag():
    tag = Tag.query.all()
    return render_template('new_tag.html', tag=tag)

@app.route('/new_tag')
def new_tag_form():
    post = Post.query.all()
    return render_template('new_tag.html', post=post)

@app.route('/new_tag')
def new_tag():
    post_id = [int(num) for num in request.form.getlist("post")]
    post = Post.query.filter(Post.id.in_(post_id)).all()
    new_tag = Tag(name=request.form['name'], post=post)

    db.session.add(new_tag)
    db.session.commit()

    return redirect("/tag")

@app.route('/tag/<int:tag_id>')
def show_tag(tag_id):
    tag= Tag.query.get_or_404(tag_id)
    return render_template('show_tag.html', tag=tag)

@app.route('/tag/<int:tag_id>/edit')
def edit_tag_form():
    tag = Tag.query.get_or_404(tag_id)
    post = Post.query.all()
    return render_template('edit_tag.html', tag=tag, post=post)

@app.route('/tag/<int:tag_id>/edit', methods=["POST"])
def edit_tag(tag_id):
    tag=Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']
    post_id = [int(num) for num in request.form.getlist("post")]
    tag.post = Post.query.filter(Post.id.in_(post_id)).all()

    db.session.add(tag)
    db.session.commit()

    return redirect("/tag")

@app.route('/tag/<int:tag_id>/delete', methods=["POST"])
def delete_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()

    return redirect("/tag")



    

