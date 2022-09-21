from unittest import TestCase

from app import app
from models import db, User

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///users_test'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UserTestCase(TestCase):
    """Tests for views for Users."""

    def setUp(self):
        """Adds a sample User"""

        User.query.delete()

        user = User(first_name="Jane", last_name="Doe", image_url="https://bruh.jpg")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

    def tearDown(self):
        """Clean up any error"""

        db.session.rollback()

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Jane', html)

    def test_show_user(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Jane', html)

    def test_add_user(self):
        with app.test_client() as client:
            d = {"firstname": "John", "lastname": "Doe", "imageurl": "https://jkhlgkjdfhlkgd.com"}
            resp = client.post("/users/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("John", html)

    def test_edit_page(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}/edit")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h4>New First Name:</h4>', html)

    def test_add_post_page(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}/posts/new")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h4>Title:</h4>', html)
            