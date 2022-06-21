from flask import Blueprint, render_template, request, flash
from .models import Post
from . import db
import requests
import markdown

# Initialize the blueprint

views = Blueprint('views', __name__)

# Set up the routes of the front end

@views.route('/')
def home():
    return render_template("base.html")

# Show the documentation

@views.route('/doc', methods=['GET'])
def documentation():
    return render_template("documentation.html")

# Show all posts

@views.route('/posts', methods=['GET'])
def posts():
    posts = Post.query.all()
    return render_template("posts.html", posts=posts)

# Add a post

@views.route('/posts/add', methods=['GET', 'POST'])
def add_post():

    new_post = None

    # If adding a post through the front end

    if request.method == 'POST':

        # Process the input from the front end input forms

        userid = request.form.get("userid")
        title = request.form.get("title")
        body = request.form.get("body")

        # Check if post meets required parameters

        try:
            if not isinstance(int(userid), int):
                flash('User Id must be an integer!', category='error')
        except ValueError:
            flash('User Id must be an integer!', category='error')
            return render_template("add_post.html")
        if len(title) < 3:
            flash('The title of your post is too short. Make sure it contains more than 3 characters.', category='error')
        if len(body) < 5:
            flash('The body of your post is too short. Make sure it contains more than 5 characters.', category='error')

        else:

            # Validate the user ID through the external API

            api_url = "http://jsonplaceholder.typicode.com/users"
            response = requests.get(api_url)
            user_list = response.json()
            user_ids = []
            for item in user_list:
                user_ids.append(item["id"])
                
            # Add post into the database

            if int(userid) in user_ids:
                new_post = Post(userid=userid, title=title, body=body)
                db.session.add(new_post)
                db.session.commit()
                flash(str('Post successfully added. Id: '+str(new_post.id)), category='success')  

            else:
                flash(str('User '+str(userid)+' is not valid.'), category='error') 

    return render_template("add_post.html", post=new_post)

# Search for post by id

@views.route('/search/id', methods=['GET', 'POST'])
def search_by_id():
    post = None

    # If searching through the front end

    if request.method == 'POST':
        id = request.form.get("id")

        # Validate the data from form

        if len(id) < 1:
            flash('Invalid id! Id must be an integer.', category='error')
            return render_template("search_id.html")
        try:
            if not isinstance(int(id), int):
                flash('Id must be an integer!', category='error')
        except ValueError:
            flash('Id must be an integer!', category='error')
            return render_template("search_id.html")

        # Add post to template to show on page

        post = Post.query.get(id)
        if post == None:
            
            # If post not found, check in external API

            api_url = "http://jsonplaceholder.typicode.com/posts"
            response = requests.get(api_url)
            posts_list = response.json()
            for post in posts_list:

                # If the post is found in the external API, restore it and save it to the database

                if int(id) == post['id']:
                    db.session.add(Post(id=post['id'], userid=post['userId'], title=post['title'], body=post['body']))
                    db.session.commit()
                    post = Post.query.get(id)
                    flash(str('Post '+str(post.id)+' restored from backup.'), category='success')
                    return render_template("search_id.html", post=post)

            flash('Post does not exist!', category='error')

    # If the post is found, display it on the page

    return render_template("search_id.html", post=post)

# Search for post by userId

@views.route('/search/userid', methods=['GET', 'POST'])
def search_by_userid():
    posts = []

    # If data entered in forms

    if request.method == 'POST':
        userid = request.form.get("userid")

        # Validate the data from form

        if len(userid) < 1:
            flash('Invalid userId! UserId must be an integer.', category='error')
            return render_template("search_userid.html")
        try:
            if not isinstance(int(userid), int):
                flash('Invalid userId! UserId must be an integer.', category='error')
        except ValueError:
            flash('UserId must be an integer!', category='error')
            return render_template("search_userid.html")

        # Add found posts into a list to show on page

        for post in db.session.query(Post).filter_by(userid=userid).all():
            posts.append(post)

        if posts == []:
            flash('User has no posts!', category='error')

    return render_template("search_userid.html", posts=posts)

# Edit a post

@views.route('/posts/edit', methods=['GET', 'POST'])
def edit():
    post = None

    # If editing through the front end

    if request.method == 'POST':
        post = request.form.get("id")

        # Validate the data from form

        if len(post) < 1:
            flash('Invalid post! Post id must be an integer.', category='error')
            return render_template("edit.html", edit=True)
        try:
            if not isinstance(int(post), int):
                flash('Post id must be an integer!', category='error')
        except ValueError:
            flash('Post id must be an integer!', category='error')
            return render_template("edit.html", edit=True)

        # If data is ok, proceed with edit

        else:

            # If Search button is pressed, show the post on the page

            if request.form.get('action') == 'Search':
                form_id = request.form.get("id")
                post = db.session.query(Post).filter_by(id=post).first()
                if post is not None:
                    flash(str('Post '+str(post.id)+' found. To proceed, input required fields and click the Edit button.'), category='success')
                    return render_template("edit.html", post=post, temp_id=post.id, edit=False)
                else:
                    flash(str('Post '+str(form_id)+' does not exist!'), category='error')

            # If Edit button is pressed, edit the post and save it in the database

            if request.form.get('action') == 'Edit':

                # Get data from input forms

                form_id = request.form.get("id")
                userid = request.form.get("userid")
                title = request.form.get("title")
                body = request.form.get("body")

                post = db.session.query(Post).filter_by(id=form_id).first()

                # Check if post meets required parameters

                try:
                    if not isinstance(int(form_id), int):
                        flash('Post Id must be an integer!', category='error')
                except ValueError:
                    flash('Post Id must be an integer!', category='error')
                    return render_template("edit.html", post=post, edit=False, temp_id=form_id, temp_userid=userid, temp_title=title, temp_body=body)
                try:
                    if not isinstance(int(form_id), int):
                        flash('User Id must be an integer!', category='error')
                except ValueError:
                    flash('User Id must be an integer!', category='error')
                    return render_template("edit.html", post=post, edit=False, temp_id=form_id, temp_userid=userid, temp_title=title, temp_body=body)
                if (len(title) < 3) and (len(body) < 5):
                    flash('The title of your post is too short. Make sure it contains more than 3 characters.', category='error')
                    flash('The body of your post is too short. Make sure it contains more than 5 characters.', category='error')
                    return render_template("edit.html", post=post, edit=False, temp_id=form_id, temp_userid=userid, temp_title=title, temp_body=body)
                if len(title) < 3:
                    flash('The title of your post is too short. Make sure it contains more than 3 characters.', category='error')
                    return render_template("edit.html", post=post, edit=False, temp_id=form_id, temp_userid=userid, temp_title=title, temp_body=body)
                if len(body) < 5:
                    flash('The body of your post is too short. Make sure it contains more than 5 characters.', category='error')
                    return render_template("edit.html", edit=False, temp_id=form_id, temp_userid=userid, temp_title=title, temp_body=body)

                post = db.session.query(Post).filter_by(id=form_id).first()

                # Check if userid is the owner of the post

                if int(userid) == post.userid:

                    # If the post exists and userid matches, check if the post changes, and if yes, edit and save it to database

                    if post is not None:
                        if post.title == title and post.body == body:
                            flash('No changes to the post were made', category='error')
                            return render_template("edit.html", post=post, edit=False, temp_id=form_id, temp_userid=userid, temp_title=title, temp_body=body)
                        post.title = title
                        post.body = body
                        db.session.commit()
                        flash('Post '+str(post.id)+' edited successfully.', category='success')
                        return render_template("edit.html", post=post, edit=True, temp_id=form_id, temp_userid=userid, temp_title=title, temp_body=body)
                    else:
                        flash('Post '+str(form_id)+' does not exist!', category='error')
                else:
                    flash('User is not the owner of the post!', category='error')
                    return render_template("edit.html", post=post, edit=False, temp_id=form_id, temp_userid=userid, temp_title=title, temp_body=body)
                    
    return render_template("edit.html", edit=True)

# Delete a post

@views.route('/posts/delete', methods=['GET', 'POST'])
def delete():
    post = None

    # If deleting through the front end

    if request.method == 'POST':
        post = request.form.get("id")

        # Validate the data from form

        if len(post) < 1:
            flash('Invalid post! Post id must be an integer.', category='error')
            return render_template("delete.html")
        try:
            if not isinstance(int(post), int):
                flash('Post id must be an integer!', category='error')
        except ValueError:
            flash('Post id must be an integer!', category='error')
            return render_template("delete.html")
        if int(post) < 1:
            flash('Post id must be a valid integer larger than 0!', category='error')
            return render_template("delete.html")

        # If data is ok, proceed with delete

        else:

            # If Search button is pressed, show the post and instructions on how to proceed

            if request.form.get('action') == 'Search':
                form_id = request.form.get("id")
                post = db.session.query(Post).filter_by(id=post).first()
                if post is not None:
                    flash(str('Post '+str(post.id)+' found. To proceed with delete click the Delete button.'), category='success')
                    return render_template("delete.html", post=post, temp_id=post.id, delete=False)
                else:
                    flash(str('Post '+str(form_id)+' does not exist!'), category='error')

            # If Delete button is pressed, display a success if post was found, or error if post does not exist

            if request.form.get('action') == 'Delete':
                form_id = request.form.get("id")
                post = db.session.query(Post).filter_by(id=post).first()
                if post is not None:
                    db.session.delete(post)
                    db.session.commit()
                    flash(str('Post '+str(post.id)+' deleted successfully.'), category='success')
                else:
                    flash(str('Post '+str(form_id)+' does not exist!'), category='error')
            
    return render_template("delete.html", post=post, delete=True)