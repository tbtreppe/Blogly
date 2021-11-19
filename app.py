"""Blogly application."""

from flask import Flask, render_template, request, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

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

@app.route('/edit', methods=["GET"])
def show_edit_form():
    return render_template('edit.html')

@app.route('/edit', methods=["POST"])
def edit_user():
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect("/user")

@app.route('/edit/Save', methods=["POST"])
def save_edit_user():
    return redirect("/user")

@app.route('/user/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
   
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/user")

@app.route('/user/<int:user_id>/new_post')
def show_new_post_form(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('new_post.html', user=user)

@app.route('/user/<int:user_id>/new_post', methods=["POST"])
def add_new_post(user_id):
    user = User.query.get_or_404(user_id)
    new_post = Post(
        title=request.form['title'],
        content=request.form['content'])

    db.session.add(new_post)
    db.session.commit()

    return redirect("/detail")

@app.route('/post/<int:post_id>')
def show_post_details(post_id):
    post = Post.query.get_or_404(user_id)
    return render_template('post_detail.html', post=post)

@app.route('/post/<int:post_id>/edit', methods=["POST"])
def edit_post():
    post = Post.query.get_or_404(post_id)
    title=request.form['title'],
    content=request.form['content']

    db.session.add(post)
    db.session.commit()

    return redirect("/user")

@app.route('/post/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
   
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()

    return redirect("/user")

    

