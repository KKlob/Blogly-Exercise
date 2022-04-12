from pydoc import HTMLDoc
from unittest import TestCase
from app import app
from models import db, User, Post

# use test database - must be created before running tests
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Make flask errors be real errors
app.config['TESTING'] = True

# Bit of a hack, don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class UserModelTestCase(TestCase):
    """Unit tests for flask routes"""

    def setUp(self):
        """Clean up any existing users"""
        User.query.delete()
        Post.query.delete()

        user = User(first_name="George", last_name="Washington", image_url="https://external-content.duckduckgo.com/iu/?u=http%3A%2F%2Fwww.americanhistorycentral.com%2Fwp-content%2Fuploads%2F2016%2F08%2Fgeorge-washington-portrait.jpg&f=1&nofb=1")
        db.session.add(user)
        db.session.commit()
        
        self.user_id = user.id

        date = Post.get_datetime()
        post = Post(title="first title", content="This is some content for the post", created_at=date, user_id=self.user_id)
        db.session.add(post)
        db.session.commit()

        self.post_id = post.id

    def tearDown(self):
        """Clean up any fouled transactions"""
        db.session.rollback()

    def test_users_homepage(self):
        with app.test_client() as client:
            resp = client.get('/', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('George Washington', html)

    def test_add_user(self):
        with app.test_client() as client:
            resp = client.post(
                '/users/new', data={
                    'first_name': 'Benjamin',
                    'last_name': 'Franklin',
                    'image_url': 'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ffthmb.tqn.com%2FRsaWt2Q5AISQWofD9SAoKWAs3fs%3D%2F2779x3583%2Ffilters%3Afill(auto%2C1)%2Fportrait-of-benjamin-franklin-boston-1706-philadelphia-1790-scientist-and-politician-ca-1785-painting-by-joseph-duplessis-siffred-1725-1802-oil-on-canvas-united-states-of-america-18th-century-540776471-58d543e93df78c51622cc444.jpg&f=1&nofb=1'
                    },
                    follow_redirects=True
                )
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Benjamin Franklin', html)

    def test_user_details(self):
        with app.test_client() as client:
            resp = client.get(f'/users/{self.user_id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('George Washington', html)
            self.assertIn("first title", html)

    def test_update_user(self):
        with app.test_client() as client:
            resp = client.post(
                f'/users/{self.user_id}/edit', data={
                    'first_name': 'Benjamin',
                    'last_name': 'Franklin',
                    'image_url': 'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ffthmb.tqn.com%2FRsaWt2Q5AISQWofD9SAoKWAs3fs%3D%2F2779x3583%2Ffilters%3Afill(auto%2C1)%2Fportrait-of-benjamin-franklin-boston-1706-philadelphia-1790-scientist-and-politician-ca-1785-painting-by-joseph-duplessis-siffred-1725-1802-oil-on-canvas-united-states-of-america-18th-century-540776471-58d543e93df78c51622cc444.jpg&f=1&nofb=1'
                    }, follow_redirects=True
                )
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Benjamin Franklin', html)

    def test_delete_user(self):
        with app.test_client() as client:
            resp = client.post(f'/users/{self.user_id}/delete', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('George Washington', html)

    def test_post_details(self):
        with app.test_client() as client:
            resp = client.get(f'/posts/{self.post_id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("first title", html)
            self.assertIn("This is some content for the post", html)

    def test_add_post(self):
        with app.test_client() as client:
            resp = client.post(f'/users/{self.user_id}/posts/new', data={
                'title': "New title",
                'content': "This is the content for new title post",
                'created_at': "Mon Jan 1 2022, 10:30 AM",
                'user_id': self.user_id}, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("New title", html)

    def test_edit_post(self):
        with app.test_client() as client:
            resp = client.post(f'/posts/{self.post_id}/edit', data={
                'title': "Title 2",
                'content': "This is some editted content",
                'created_at': "Mon Jan 1 2022, 10:30 AM"}, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Title 2', html)
            self.assertNotIn('first title', html)

    def test_delete_post(self):
        with app.test_client() as client:
            resp = client.post(f'/posts/{self.post_id}/delete', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('first title', html)