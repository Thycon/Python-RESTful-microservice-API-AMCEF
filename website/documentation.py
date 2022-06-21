from flask import Blueprint, render_template

documentation = Blueprint('documentation', __name__)

@documentation.route('/', methods=['GET'])
def show_documentation():
    return render_template("documentation.html")