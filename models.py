"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """User."""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                    primary_key=True)
    first_name = db.Column(db.String(50),
                            nullable=False)
    last_name = db.Column(db.String(50),
                            nullable=False)
    image_url = db.Column(db.String,
                            nullable=False,
                            default="https://t4.ftcdn.net/jpg/00/64/67/63/360_F_64676383_LdbmhiNM6Ypzb3FM4PPuFP9rHe7ri8Ju.jpg")
    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")

    def __repr__(self):
        """Show info about user."""

        u = self
        return f"<User {u.id} {u.first_name} {u.last_name} {u.image_url}"

    def edit(self, first, last, image):
        """Edits a users profile"""

        self.first_name = first
        self.last_name = last
        self.image_url = image

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

class Post(db.Model):
    """Post."""

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    tags = db.relationship('Tag',
                            secondary='post_tags',
                            backref='posts')

    def edit(self, title, content):
        """Edits a post content"""

        self.title = title
        self.content = content

class Tag(db.Model):
    """Tag."""

    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)

    def edit(self, name):
        """Edits a tag name"""

        self.name = name

class PostTag(db.Model):
    """PostTag."""

    __tablename__ = "post_tags"

    post_id = db.Column(db.Integer,
                        db.ForeignKey('posts.id'),
                        primary_key=True)
    tag_id = db.Column(db.Integer,
                        db.ForeignKey('tags.id'),
                        primary_key=True)

def connect_db(app):
    """Connect to database"""

    db.app = app
    db.init_app(app)