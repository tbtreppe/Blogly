"""Blogly application."""

from flask import Flask, render_template, request, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///blogly"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "secrets"
app.config ['DEBUG_TB_INTERCEPT_REDIRECTS']= False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/user')
def list_users():
    user = User.query.all()
    return render_template('new_user.html', user=user)

@app.route('/new_user', methods=["POST"])
def add_new_user():
    firstname = request.form["First Name"]
    lastname = request.form["Last Name"]
    imageurl = request.form ["Image URL"]

    new_user = User(firstname=firstname, lastname=lastname, imageurl=imageurl)
    db.session.add(new_user)
    db.session.commit()

    return redirect (f'/{new_user.id}')

@app.route("/int:user_id")
def show_user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("details.html", user=user)