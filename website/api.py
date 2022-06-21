from flask_restful import reqparse
from .models import Post
from flask import Blueprint, request
from . import db
import requests
import json

api = Blueprint('api', __name__)

# Route for displaying all posts and adding a new post

@api.route('/posts', methods=['GET', 'POST'])
def posts():

    # Add a new post

    if str(request.method) == 'POST':

        # Parse the POST request data

        parser = reqparse.RequestParser()
            
        parser.add_argument('userId', type=int, required=True)
        parser.add_argument('title', type=str, required=True)
        parser.add_argument('body', type=str, required=True)

        args = parser.parse_args()

        # Validate the POST data

        if len(args["title"]) < 3:
            return {'error': 'title is too short - title has to be at least 3 characters'}
        if len(args["body"]) < 5:
            return {'error': 'body is too short - title has to be at least 5 characters'}

        # Validate the userId

        api_url = "http://jsonplaceholder.typicode.com/users"
        response = requests.get(api_url)
        user_list = response.json()
        user_ids = []
        for item in user_list:
            user_ids.append(item["id"])

        if int(args["userId"]) not in user_ids:
            return {'error': 'userid is not valid'}

        # Add post into the database

        new_post = Post(userid=args["userId"], title=args["title"], body=args["body"])
        db.session.add(new_post)
        db.session.commit()

        data = {"id": new_post.id, "userId": new_post.userid, "title": new_post.title, "body": new_post.body}

        return json.dumps({'message': 'Post successfully added.', 'data': data}, indent=2), 201

    # Otherwise handle the GET request

    data = []
    posts = Post.query.all()
        
    for post in posts:
        data.append({"id": post.id, "userId": post.userid, "title": post.title, "body": post.body})

    return json.dumps({'message': 'Success', 'data': data}, indent=2), 200

# Search, delete, edit post by id

@api.route('/posts/<string:id>', methods=['GET', 'DELETE', 'PUT'])
def post(id):

    post_id = Post.query.get(id)
    post = None

    # Delete the post

    if request.method == 'DELETE':

        # Validate the id/link

        if len(id) < 1:
            return {'error': 'Invalid post! Post id must be an integer'}
        try:
            if not isinstance(int(id), int):
                return {'error': 'Invalid post! Post id must be an integer'}
        except ValueError:
            return {'error': 'Post id must be an integer!'}

        # If data is ok, proceed with delete

        else:

            # Proceed with deleting the post

            post = db.session.query(Post).filter_by(id=id).first()

            if post is not None:
                db.session.delete(post)
                db.session.commit()
                return {'message': str('Post '+str(id)+' deleted successfully')}, 200
            else:
                return json.dumps({'message': 'Post not found', 'data': {}},indent=2), 404

    # Edit the post

    if request.method == 'PUT':

        # Validate the id/link

        if len(id) < 1:
            return {'error': 'Invalid post! Post id must be an integer'}
        try:
            if not isinstance(int(id), int):
                return {'error': 'Invalid post! Post id must be an integer'}
        except ValueError:
            return {'error': 'Post id must be an integer!'}
        
        if post_id is None:
            return {'message': 'Post does not exist!'}, 404

        # If data is ok, proceed with edit

        else:

            # Parse the data from PUT request
            
            parser = reqparse.RequestParser()
            
            parser.add_argument('userId', type=int, required=True)
            parser.add_argument('title', type=str, required=True)
            parser.add_argument('body', type=str, required=True)

            args = parser.parse_args()

            # Find the post in database

            post = db.session.query(Post).get(id)

            # Check if user is the owner of the post

            if post.userid != args['userId']:
                return {'error': 'user is not the owner of the post'}

            # Check if the post meets required parameters

            if (len(args["title"]) < 3) and (len(args["body"]) < 5):
                return {'error': ['title is too short - title has to be at least 3 characters', 'body is too short - body has to be at least 5 characters']}
            if len(args["title"]) < 3:
                return {'error': 'title is too short - title has to be at least 3 characters'}
            if len(args["body"]) < 5:
                return {'error': 'body is too short - body has to be at least 5 characters'}

            # Check if the post changed

            if (post.title == args["title"]) and (post.body == args["body"]):
                return json.dumps({'message': 'arguments match the post - no changes to the post were made', 'data': args},indent=2), 200

            # Edit the post and save it into database

            post.title = args["title"]
            post.body = args["body"]
            db.session.commit()
            return json.dumps({'message': 'Post '+str(id)+' successfully edited', 'data': args},indent=2), 200

    # Otherwise handle the GET request

    if post_id is not None:

        # Post found in database

        return json.dumps({'message': 'Post found', 'data': {"userid": post_id.userid, "title": post_id.title, "body": post_id.body}}, indent=2), 200
    
    else:

        # If post not found, check if it can be restored from backup

        api_url = "http://jsonplaceholder.typicode.com/posts"
        response = requests.get(api_url)
        posts_list = response.json()
        for post in posts_list:
            if int(id) == post['id']:
                db.session.add(Post(id=post['id'], userid=post['userId'], title=post['title'], body=post['body']))
                db.session.commit()
                return json.dumps({'message': str('Post '+id+' was restored from backup'), 'data': {"id": post['id'], "userId": post['userId'], "title": post['title'], "body": post['body']}}, indent=2), 201

        return json.dumps({'message': 'Post not found', 'data': {}}, indent=2), 404

# Search posts by userId

@api.route('/userposts/<string:userid>')
def get_user_posts(userid):
    posts = []

    # Validate the data from form

    if len(userid) < 1:
        return {'error': 'Invalid userId! UserId must be an integer.'}
    try:
        if not isinstance(int(userid), int):
            return {'error': 'Invalid userId! UserId must be an integer.'}
    except ValueError:
        return {'error': 'Invalid userId! UserId must be an integer.'}

    # Add found posts into a list to show on page

    for post in db.session.query(Post).filter_by(userid=userid).all():
        posts.append({"id": post.id, "userid": post.userid, "title": post.title, "body": post.body})

        # Return a 404 if the user has no posts

        if posts == []:
            return {'error': 'User has no posts!'}, 404

    # Return posts from user

    return json.dumps({'message': 'success', 'data': posts}), 200