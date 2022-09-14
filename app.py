"""Blogly application."""

from flask import Flask, request, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

@app.route('/')
def home_page():
    """Redirect users to list of users page"""
    return redirect('/users')

@app.route('/users')
def users_page():
    """Shows list of all users"""

    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/users/new')
def new_user_page():
    return render_template('new.html')

@app.route('/users/new', methods=["POST"])
def add_user():
    """Add user to list"""

    first = request.form['firstname']
    last = request.form['lastname']
    image = request.form['imageurl']

    user = User(first_name=first, last_name=last, image_url=image)
    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:userid>')
def more_info(userid):
    """Shows more information about a user"""

    user = User.query.get_or_404(userid)
    return render_template('user.html', user=user)

@app.route('/users/<int:userid>/edit')
def edit_user_form(userid):
    """Shows user edit page"""

    user = User.query.get_or_404(userid)
    return render_template('useredit.html', user=user)

@app.route('/users/<int:userid>/edit', methods=["POST"])
def edit_user(userid):
    """Edits specified user"""

    user = User.query.get_or_404(userid)
    first = request.form['firstname']
    last = request.form['lastname']
    image = request.form['imageurl']

    user.edit(first=first, last=last, image=image)

    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:userid>/delete', methods=["POST"])
def delete_user(userid):
    """Deletes specified user"""

    del_user = User.query.get_or_404(userid)

    db.session.delete(del_user)
    db.session.commit()

    return redirect('/users')

