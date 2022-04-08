from pydoc import HTMLDoc
from unittest import TestCase
from app import app
from models import db, User

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

        user = User(first_name="George", last_name="Washington", image_url="https://external-content.duckduckgo.com/iu/?u=http%3A%2F%2Fwww.americanhistorycentral.com%2Fwp-content%2Fuploads%2F2016%2F08%2Fgeorge-washington-portrait.jpg&f=1&nofb=1")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

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
            self.assertIn('<h2>George Washington</h2>', html)

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