"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

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