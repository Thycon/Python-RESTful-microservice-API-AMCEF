from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from json import JSONDecodeError
import requests
from os import path

# Define the database object

db = SQLAlchemy()
DB_NAME = "posts.db"

# Create the Flask website app

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '1_R34LLY_W4NT_TH15_J08_:)'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    # Initialize the database, and register blueprint routes

    with app.app_context():
        db.init_app(app)
        from .views import views
        from .api import api

        app.register_blueprint(views, url_prefix='/')
        app.register_blueprint(api, url_prefix='/api')

        from .models import Post

        # If the database was created for the first time, initialize data from the external API

        @event.listens_for(Post.__table__, 'after_create')
        def initialize_database_from_external_api(*args, **kwargs):
            from .models import Post
            posts = Post.query.all()
            api_url = "http://jsonplaceholder.typicode.com/posts"
            response = requests.get(api_url)
            posts_list = response.json()
            for post in posts_list:
                db.session.add(Post(id=post['id'], userid=post['userId'], title=post['title'], body=post['body']))
            db.session.commit()

        create_database(app)

    return app

# Create the database

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')