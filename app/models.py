from app import db, bcrypt
from flask import current_app
from datetime import datetime, timedelta
from markdown import markdown
import bleach



class Author(db.Model):
    """This class defines the author table """

    __tablename__ = 'author'

    id            = db.Column(db.Integer, primary_key=True)
    ip_address    = db.Column(db.Text, nullable=False, unique=True)
    created_at    = db.Column(db.DateTime, default=db.func.current_timestamp())
    modified_at   = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())

    # Relations
    posts        = db.relationship('Post', order_by='Post.id', backref='author', lazy=True)
    votes        = db.relationship('Vote', order_by='Vote.id', backref='author', lazy=True)

    def __init__(self, ip_address):
        """Initialize the Autor with a ip_address."""

        self.ip_address = ip_address 


    def save(self):
        """
        Saves a USER to the database.
        This includes creating a new USER and editing one.
        """

        db.session.add(self)
        db.session.commit()

class Post(db.Model):
    """This class defines the Post table """

    __tablename__ = 'post'

    # Define the columns of the Post table, starting with the primary key
    id            = db.Column(db.Integer, primary_key=True)
    content       = db.Column(db.Text, nullable=True)
    parent_id     = db.Column(db.Integer)
    author_id     = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
    created_at    = db.Column(db.DateTime, default=db.func.current_timestamp())
    modified_at   = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())

    # relations
    votes = db.relationship('Vote', order_by='Vote.id', backref='post', lazy=True)
    
    
    def __init__(self, content, author_id, parent_id=0):
        """Initialize the Readme."""

        self.content = content
        self.author_id = author_id
        self.parent_id = parent_id

    def to_dict(self):
        return {
            "id":self.id,
            "content": self.content,
            "created_at" : self.created_at
        }

    def  content_html(self):
        html = markdown(bleach.linkify(self.content))

        attrs = {
            '*'  : ['class', 'title', 'id'],
            'a'  : ['href', 'rel'],
            'img': ['alt','src']
        }

        tags = ["h1", "h2", "h3", "h4" , "h5", "h6", 
                "em", "i", "strong", "code", "p", "a",
                "ul", "ol", "li", "img", "pre", "nav", "div",
                "article", "pre", "span", "blockquote"]

        html = bleach.clean(
            html,
            tags=tags,
            protocols=['http', 'https', 'mailto'],
            attributes=attrs,
            strip_comments=True
        )

        return html


    def has_voted(self, author_id):
        vote = Vote.query.filter_by(author_id=author_id, post_id=self.id).first()
        return bool(vote)

    def get_replies(self):
        return Post.query.filter_by(parent_id=self.id).all()

    def has_voted(self, author_id):
        vote = Vote.query.filter_by(author_id=author_id, post_id=self.id).first()
        return bool(vote)
    
    def save(self):
        """
        Saves a Post to the database.
        This includes creating a new Post and editing one.
        """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Vote(db.Model):
    """This class defines the Vote table """

    __tablename__ = 'vote'

    # Define the columns of the Vote table, starting with the primary key
    id            = db.Column(db.Integer, primary_key=True)
    value         = db.Column(db.Integer, nullable=False)
    post_id       = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    author_id     = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
    created_at    = db.Column(db.DateTime, default=db.func.current_timestamp())
    modified_at   = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())

    deleted     = db.Column(db.Boolean, default=False)
    
    def __init__(self, value, post_id, author_id):
        self.value   = value
        self.post_id = post_id
        self.author_id = author_id

    
    def save(self):
        """Save an Vote to the database."""

        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
