"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm  import backref
from datetime import datetime

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)



class User(db.Model):
    """User"""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    first_name = db.Column(db.String(50),
                    nullable=False)
    last_name = db.Column(db.String(50),
                    nullable=False)
    image_url = db.Column(db.Text)

    def __repr__(self):
        """Show info about user"""

        u = self
        return f"<User ID: {u.id} | first_name: {u.first_name} | last_name: {u.last_name} | image_urg: {u.image_url}>"

    @classmethod
    def get_all_users(self):
        return list(User.query.order_by(User.last_name, User.first_name).all())

    @classmethod
    def get_user(self, userID):
        return User.query.get(userID)

    @classmethod
    def add_new_user(self, first, last, img):
        user = User(first_name=first, last_name=last, image_url=img)
        db.session.add(user)
        db.session.commit()

    @classmethod
    def update_user(self, id, first, last, img):
        user = self.get_user(id)
        user.first_name = first
        user.last_name = last
        user.image_url = img
        db.session.add(user)
        db.session.commit()

    @classmethod
    def remove_user(self, userID):
        user = self.get_user(userID)
        db.session.delete(user)
        db.session.commit()

class Post(db.Model):
    """Posts"""

    __tablename__ = "posts"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    title = db.Column(db.String(100),
                    nullable=False)
    content = db.Column(db.Text,
                    nullable=False)
    created_at = db.Column(db.Text,
                    nullable=False)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id', ondelete='CASCADE'))

    user = db.relationship('User', backref="posts")

    def __repr__(self):
        """Show info about the post"""

        p = self
        return f"<Post ID: {p.id} | title: {p.title} | content: {p.content} | created_at: {p.created_at} | user_id: {p.user_id} >"

    @classmethod
    def get_all_posts(self, userID):
        return list(Post.query.filter(Post.user_id == userID).all())
    
    @classmethod
    def get_post(self, postID):
        return Post.query.get(postID)

    @classmethod
    def add_new_post(self, title, content, date, userID):
        post = Post(title=title, content=content, created_at=date, user_id=userID)
        db.session.add(post)
        db.session.commit()

    @classmethod
    def update_post(self, title, content, date, postID):
        post = self.get_post(postID)
        post.title = title
        post.content = content
        post.created_at = date
        userID = post.user_id
        db.session.add(post)
        db.session.commit()
        return userID

    @classmethod
    def delete_post(self, postID):
        post = self.get_post(postID)
        userID = post.user_id
        db.session.delete(post)
        db.session.commit()
        return userID

    @classmethod
    def get_datetime(self):
        return datetime.now().strftime("%a %b %d %Y, %I:%M %p")
       