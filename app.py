"""Blogly application."""

from flask import Flask, request, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

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

@app.route('/users/<int:userid>/posts/new', methods=["GET"])
def new_post_form(userid):
    """Gives user a form to submit a new post"""

    user = User.query.get_or_404(userid)

    return render_template('newpostform.html', user=user)

@app.route('/users/<int:userid>/posts/new', methods=["POST"])
def post_form(userid):
    """Gets form content and makes a post, saves to database"""

    user = User.query.get_or_404(userid)
    post_title = request.form['title']
    post_content = request.form['content']

    post = Post(title=post_title, content=post_content, user=user)
    db.session.add(post)
    db.session.commit()

    return redirect(f"/users/{userid}")

@app.route('/posts/<int:postid>')
def view_post(postid):
    """Views post of postid"""

    post = Post.query.get_or_404(postid)

    return render_template('post.html', post=post)

@app.route('/posts/<int:postid>/edit')
def view_post_edit(postid):
    """Give form to edit a post"""

    post = Post.query.get_or_404(postid)

    return render_template('postedit.html', post=post)

@app.route('/posts/<int:postid>/edit', methods=["POST"])
def post_edit_submission(postid):
    """Edit a specific post with given contents"""

    post = Post.query.get_or_404(postid)
    title = request.form['title']
    content = request.form['content']

    post.edit(title=title, content=content)

    db.session.commit()

    return redirect(f'/posts/{postid}')

@app.route('/posts/<int:postid>/delete', methods=["POST"])
def delete_post(postid):
    """Deletes specified post"""

    del_post = Post.query.get_or_404(postid)

    db.session.delete(del_post)
    db.session.commit()

    return redirect('/users')