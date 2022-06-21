from . import db

# Define the post parameters as a db.Model

class Post(db.Model):
    __tablename__ = "post"
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer)
    title = db.Column(db.String(50))
    body = db.Column(db.String(250))
