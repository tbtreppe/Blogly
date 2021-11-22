"""Models for Blogly."""
import datetime
from flask_sqlalchemy import SQLAlchemy 
db = SQLAlchemy()

class User(db.Model):
    __tablename__= "user"

    
        
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, nullable=False)
    post = db.relationship("Post", backref="user")



class Post(db.Model):
    __tablename__="post"

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.Text, nullable=False, unique=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default= datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class PostTag(db.Model):
    __tablename__="post_tag"

    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'), primary_key=True)

class Tag(db.Model):
    __tablename__="tag"

    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.Text, nullable=False, unique=True)

    post = db.relationship('Post', secondary = "post_tag", backref = "tag")


def connect_db(app):
    db.app=app
    db.init_app(app)    


