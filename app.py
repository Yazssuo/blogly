"""Blogly application."""

from flask import Flask, request, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag

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
    tags = Tag.query.all()

    return render_template('newpostform.html', user=user, tags=tags)

@app.route('/users/<int:userid>/posts/new', methods=["POST"])
def post_form(userid):
    """Gets form content and makes a post, saves to database"""

    user = User.query.get_or_404(userid)
    post_title = request.form['title']
    post_content = request.form['content']

    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()


    post = Post(title=post_title, content=post_content, user=user, tags=tags)
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
    tags = Tag.query.all()

    return render_template('postedit.html', post=post, tags=tags)

@app.route('/posts/<int:postid>/edit', methods=["POST"])
def post_edit_submission(postid):
    """Edit a specific post with given contents"""

    post = Post.query.get_or_404(postid)
    title = request.form['title']
    content = request.form['content']

    post.edit(title=title, content=content)

    tag_ids = [int(num) for num in request.form.getlist("tags")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    db.session.commit()

    return redirect(f'/posts/{postid}')

@app.route('/posts/<int:postid>/delete', methods=["POST"])
def delete_post(postid):
    """Deletes specified post"""

    del_post = Post.query.get_or_404(postid)

    db.session.delete(del_post)
    db.session.commit()

    return redirect('/users')

@app.route('/tags')
def view_tags():
    """Lists all tags"""

    tags = Tag.query.all()

    return render_template('tags.html', tags=tags)

@app.route('/tags/<int:tagid>')
def view_tag(tagid):
    """Views specific tag"""

    tag = Tag.query.get_or_404(tagid)
    tag_name = tag.name
    tag_posts = tag.posts

    return render_template('tag.html', name=tag_name, posts=tag_posts, id=tag.id)

@app.route('/tags/<int:tagid>/edit')
def edit_tag_form(tagid):
    """Gives user tag form to edit it"""

    tag = Tag.query.get_or_404(tagid)

    return render_template('edittag.html', tag=tag)

@app.route('/tags/<int:tagid>/edit', methods=["POST"])
def edit_tag(tagid):
    """Changes specified tag name"""

    tag = Tag.query.get_or_404(tagid)
    name = request.form['tagname']

    tag.edit(name=name)

    db.session.commit()

    return redirect('/tags')

@app.route('/tags/new')
def tag_form():
    """Gives user tag form"""

    return render_template('addtag.html')

@app.route('/tags/new', methods=["POST"])
def add_tag():
    """Adds tag to database"""

    tag_name = request.form['tagname']
    tag = Tag(name=tag_name)

    db.session.add(tag)
    db.session.commit()

    return redirect('/tags')

@app.route('/tags/<int:tagid>/delete', methods=["POST"])
def del_tag(tagid):
    """Deletes tag from database"""

    del_tag = Tag.query.get_or_404(tagid)

    db.session.delete(del_tag)
    db.session.commit()

    return redirect('/tags')