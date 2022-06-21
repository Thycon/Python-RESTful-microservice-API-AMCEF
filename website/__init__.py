from flask import Flask,g
from flask_restful import Resource,Api,reqparse
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
import json
from json import JSONDecodeError
import requests
from os import path

# Create the database object
db = SQLAlchemy()
DB_NAME = "posts.db"

# Creating a Flask website app
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '1_R34LLY_W4NT_TH15_J08_:)'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    with app.app_context():
        db.init_app(app)

        from .views import views
        from .documentation import documentation

        app.register_blueprint(views, url_prefix='/')
        app.register_blueprint(documentation, url_prefix='/documentation')

        from .models import Post
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

# Initialize the database
def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
        
# from .models import Post


# class Posts(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     userId = db.Column(db.Integer)
#     title = db.Column(db.String(69), unique=True, nullable=False)
#     body = db.Column(db.String(420), unique=True, nullable=False)
#     def __repr__(self):
#         return f"{self.title} - {self.body}"
    
# @app.route('/')
# def index():
#     """ Present the documentation"""
    
#     with open(os.path.dirname(app.root_path) + '/ReadMe.txt', 'r') as markdown_file:
        
#         content = markdown_file.read()
#         return markdown.markdown(content)
    
# # def get_db():
# #     db = getattr(g, '_database', None)
# #     data = {}
# #     if db is None:
# #         # db = g._database = shelve.open("posts.db")
# #         for item in posts_list:
# #             data.update({item['id']:item})
            
# #             shelf[args['id']] = args
# #         db = g._database = data
# #     return db
# def initialize_database():
#     with open('database.json', 'w') as file:
#         data = {}
#         for item in posts_list:
#             data.update({item['id']:item})
#         json.dump(data, file, indent=2)
#     with open('database.json', 'r') as file:
#         return json.load(file)
    
# def update_database(data):
#     with open('database.json', 'w') as file:
#         json.dump(data, file, indent=2)

# def get_db():
#     try:
#         with open('database.json', 'r') as file:
#             try:
#                 db = json.load(file)
#             except JSONDecodeError:
#                 db = initialize_database()
#             return db
#     except FileNotFoundError:
#         db = initialize_database()
#         return db
    
# # @app.teardown_appcontext
# # def teardown_db(exception):
# #     db = getattr(g, '_database', None)
# #     if db is not None:
# #         db.close()

# # class SchemaValidator(object):
# #     def __init__(self, response={}):
# #         self.response = response
        
# #     def isTrue(self):
        
# #         errorMessages = []
        
# #         try:
# #             identifier = self.response.get("id", None)
# #             if identifier is None or len(identifier) <= 1:
# #                 raise Exception("Error")
# #         except Exception as e:errorMessages.append("Field id is required")
        
# #         return errorMessages

# def data_validation(value, idx):
#     try:
#         x = value(**value)
#     except TypeError:
#         raise ValueError("Invalid data type!")
#     except:
#         raise ValueError

#     return x

# class PostsList(Resource):
#     def get(self):
#         database = get_db()
#         keys = list(database.keys())
        
#         posts = []
        
#         for key in keys:
#             posts.append(database[key])
            
#         return {'message': 'Success', 'data': posts}
    
#     def post(self):
#         parser = reqparse.RequestParser()
        
#         parser.add_argument('id', type=int, required=True)
#         parser.add_argument('userId', type=int, required=True)
#         parser.add_argument('title', type=str, required=True)
#         parser.add_argument('body', type=str, required=True)
        
#         args = parser.parse_args()
        
#         if not isinstance(args["userId"], int):
#             return {'error': 'userId must be an integer!'}
#         if not isinstance( args["id"], int):
#             return {'error': 'id must be an integer!'}
#         if not isinstance(args["title"], str):
#             return {'error': 'title must be a string!'}
#         if not isinstance(args["body"], str):
#             return {'error': 'body must be a string!'}
        
#         database = get_db()
#         item = {"userId":args["userId"], "id": args["id"], "title": args["title"], "body": args["body"]}
#         database.update({"":item})
#         update_database(database)
        
#         return {'message': 'Post added', 'data': args}, 201
    
#     def put(self):
        
#         database = get_db()
        
#         parser = reqparse.RequestParser()
        
#         parser.add_argument('id', type=int, required=True)
#         parser.add_argument('userId', type=int, required=True)
#         parser.add_argument('title', type=str, required=True)
#         parser.add_argument('body', type=str, required=True)
        
#         args = parser.parse_args()
        
#         if not isinstance(args["userId"], int):
#             return {'error': 'userId must be an integer!'}
#         if not isinstance( args["id"], int):
#             return {'error': 'id must be an integer!'}
#         if not isinstance(args["title"], str):
#             return {'error': 'title must be a string!'}
#         if not isinstance(args["body"], str):
#             return {'error': 'body must be a string!'}
        
#         for item in database:
#             if int(database[item]["id"]) == int(args["id"]):
#                 if database[item]["userId"] != args["userId"]:
#                     return{'error': 'your user is not owner of this post'}
#                 database[item]["title"] = args["title"]
#                 database[item]["body"] = args["body"]
#                 update_database(database)
#                 return{"message": "post successfully updated", "data": database[item]}
        
    
# class Post(Resource):
#     def get(self, id):
#         database = get_db()
        
#         for item in database:
#             if int(database[item]["id"]) == int(id):
#                 return {'message': 'Post found', 'data': database[item]}, 200
#         for item in posts_list:
#             if int(id) == item["id"]:
#                 database.update({item["id"]:item})
#                 update_database(database)
#                 return{'message': "Post was found in backup", 'data': item}, 404
        
#         return{'message': 'Post not found', 'data': {}}, 404
#         # return {'message': 'Post found', 'data': database[id]}, 200
    
#     def delete(self, id):
#         database = get_db()
        
#         for item in database:
#             if int(database[item]["id"]) == int(id):
#         # if not (id in database):
#                 del database[item]
#                 update_database(database)
#                 return {'message': str('Post '+str(id)+' deleted successfully')}
#         return{'message': 'Post not found', 'data': {}}, 404
    
# class UserPost(Resource):
#     def get(self, id):
#         database = get_db()
#         posts = []
        
#         for item in database:
#             if int(database[item]["userId"]) == int(id):
#                 posts.append(database[item])
#         if posts != []:
#             return {'message': 'Users posts found', 'data': posts}, 200
#         return{'message': "User doesn't have any posts!", 'data': {}}, 404
    
# api.add_resource(PostsList, '/posts')
# api.add_resource(Post, '/post/<string:id>')
# api.add_resource(UserPost, '/user/<string:id>')

# def debug_entry(message):
    
#     with open('debug.txt', 'a', encoding='utf-8') as debug:
#         debug.write(message+'\n')