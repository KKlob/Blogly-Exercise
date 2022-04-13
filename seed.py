"""Seed file to make sample data for blogly db"""

from models import User, Post, Tag, PostTag, db
from app import app

# create all tables
db.drop_all()
db.create_all()

# if table isn't empty, empty it
User.query.delete()
Post.query.delete()
Tag.query.delete()
PostTag.query.delete()
# add users

bob = User(first_name="Bob", last_name="The Builder", image_url="https://external-content.duckduckgo.com/iu/?u=http%3A%2F%2Fimages.genius.com%2F2f7a910abff8cfdfdd91751a4edd6f2a.1000x1000x1.jpg&f=1&nofb=1")
george = User(first_name="George", last_name="Washington", image_url="https://external-content.duckduckgo.com/iu/?u=http%3A%2F%2Fwww.americanhistorycentral.com%2Fwp-content%2Fuploads%2F2016%2F08%2Fgeorge-washington-portrait.jpg&f=1&nofb=1")

# Add new objects to session so they persist
db.session.add(bob)
db.session.add(george)

# Commit to db
db.session.commit()

# add posts
date = Post.get_datetime()
post1 = Post(title="my title", content="This is some content", created_at=date, user_id=1)
post2 = Post(title="my title", content="This is some content", created_at=date, user_id=2)

# add new objects to session
db.session.add(post1)
db.session.add(post2)

#commit to db
db.session.commit()

# create new tags

tag1 = Tag(name="happy")
tag2 = Tag(name="funny")

# append tags to posts via relationship to fill both tags table and posts_tags table
post = Post.query.get(1)
post.tags.append(tag1)
db.session.add(post)

post2 = Post.query.get(2)
post2.tags.append(tag2)
post2.tags.append(tag1)
db.session.add(post2)

#commit to db
db.session.commit()
    