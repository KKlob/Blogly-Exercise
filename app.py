"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag


# Config app stuff
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'doifhaofhnaifj'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
#debug = DebugToolbarExtension(app)

# connect db to app and create all tables
connect_db(app)

@app.route('/')
def redirect_to_user_homepage():
    """Redirects to users homepage"""
    return redirect('/users')

@app.route('/users')
def user_homepage():
    """Shows list of all users"""
    users = User.get_all_users()
    return render_template('users_page.jinja', users=users)

@app.route('/users/new')
def add_user_page():
    """Shows the add_user form"""
    return render_template('add_user_form.jinja')

@app.route('/users/new', methods=["POST"])
def add_user():
    """Captures form data and adds user to db"""
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']
    User.add_new_user(first_name, last_name, image_url)
    return redirect('/users')

@app.route('/users/<userID>')
def user_infopage(userID):
    """Shows user information"""
    user = User.get_user(userID)
    posts = Post.get_all_posts(userID)
    return render_template('user_detail_page.jinja', user=user, posts=posts)

@app.route('/users/<userID>/edit')
def edit_user_page(userID):
    """Shows edit_user form"""
    user = User.get_user(userID)
    return render_template('edit_user_form.jinja', user=user)

@app.route('/users/<userID>/edit', methods=["POST"])
def edit_user(userID):
    """ Captures edits to user and updates db"""
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']
    User.update_user(userID, first_name, last_name, image_url)
    return redirect('/users')

@app.route('/users/<userID>/delete', methods=["POST"])
def delete_user(userID):
    """Removes user from db"""
    User.remove_user(userID)
    return redirect ('/users')

@app.route('/posts/<postID>')
def post_page(postID):
    post = Post.get_post(postID)
    return render_template("post_details.jinja", post=post)

@app.route('/users/<userID>/posts/new')
def add_new_post_page(userID):
    """Shows form to add new post"""
    user = User.get_user(userID)
    tags = Tag.get_all_tags()
    return render_template("add_post_form.jinja", userID=userID, user=user, tags=tags)

@app.route('/users/<userID>/posts/new', methods=["POST"])
def add_new_post(userID):
    """Captures form data and adds new post"""
    title = request.form['title']
    content = request.form['content']
    tags_list = request.form.getlist('tags_checklist')
    date = Post.get_datetime()
    postID = Post.add_new_post(title,content,date,userID)
    PostTag.update_tags_on_post(postID, tags_list)
    return redirect(f'/users/{userID}')

@app.route('/posts/<postID>/edit')
def edit_post(postID):
    """Show form to edit an existing post"""
    post = Post.get_post(postID)
    user = post.user.first_name + " " + post.user.last_name
    tags = Tag.get_all_tags()
    return render_template("edit_post.jinja", post=post, user=user, tags=tags)

@app.route('/posts/<postID>/edit', methods=["POST"])
def update_post(postID):
    """Capture form values and update post in db"""
    title = request.form['title']
    content = request.form['content']
    tags_list = request.form.getlist('tags_checklist')
    date = Post.get_datetime()
    userID = Post.update_post(title, content, date, postID)
    PostTag.update_tags_on_post(postID, tags_list)
    return redirect(f'/users/{userID}')

@app.route('/posts/<postID>/delete', methods=["POST"])
def delete_post(postID):
    """Delete selected post"""
    userID = Post.delete_post(postID)
    return redirect(f'/users/{userID}')

@app.route('/tags')
def tags_list_page():
    """Lists all tags, with links to tag detail page"""
    tags = Tag.get_all_tags()
    return render_template("tags_list.jinja", tags=tags)

@app.route('/tags/<tagID>')
def tag_details_page(tagID):
    """Shows details of selected tag"""
    tag = Tag.get_tag(tagID)
    return render_template('tag_details.jinja', tag=tag)

@app.route('/tags/new')
def add_tag_page():
    """Show form to add a new tag"""
    return render_template("add_tag_form.jinja")

@app.route('/tags/new', methods=["POST"])
def add_tag():
    """Captures form value and adds new tag to db"""
    name = request.form['tag_name']
    Tag.add_tag(name)
    return redirect('/tags')

@app.route('/tags/<tagID>/edit')
def edit_tag_page(tagID):
    """Shows form to edit selected tag"""
    tag = Tag.get_tag(tagID)
    return render_template("edit_tag.jinja", tag=tag)

@app.route('/tags/<tagID>/edit', methods=["POST"])
def edit_tag(tagID):
    """Captures form value and updates existing tag in db"""
    name = request.form['tag_name']
    Tag.update_tag(name, tagID)
    return redirect('/tags')

@app.route('/tags/<tagID>/delete', methods=["POST"])
def delete_tag(tagID):
    """Deletes selected tag from db and redirects to tags list"""
    Tag.remove_tag(tagID)
    return redirect('/tags')