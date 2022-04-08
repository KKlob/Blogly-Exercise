"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User


# Config app stuff
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'doifhaofhnaifj'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

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
    return render_template('user_detail_page.jinja',user=user)

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

