from unittest import TestCase

from app import app, db
from models import User, connect_db, Post

# Let's configure our app to use a different database for tests
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///blogly_test"

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

connect_db(app)
db.create_all()


class UserViewTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""

        # As you add more models later in the exercise, you'll want to delete
        # all of their records before each test just as we're doing with the
        # User model below.
        Post.query.delete()
        User.query.delete()

        self.client = app.test_client()

        test_user = User(
            first_name="test_first",
            last_name="test_last",
            image_url=None,
        )

        second_user = User(
            first_name="test_first_two",
            last_name="test_last_two",
            image_url=None,
        )

        db.session.add_all([test_user, second_user])
        db.session.commit()

        # We can hold onto our test_user's id by attaching it to self (which is
        # accessible throughout this test class). This way, we'll be able to
        # rely on this user in our tests without needing to know the numeric
        # value of their id, since it will change each time our tests are run.
        self.user_id = test_user.id

        test_user_post = Post(
            title='Post for Test User',
            content='Content for test user.',
            user_id=self.user_id
        )

        db.session.add_all([test_user_post])
        db.session.commit()

        self.post_id = test_user_post.id

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_list_users(self):
        """ Tests that user list renders """
        with self.client as c:
            resp = c.get("/users")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("test_first", html)
            self.assertIn("test_last", html)

    def test_add_new_user(self):
        """ Test that a new user gets added to users list"""
        with self.client as c:
            data = {
                'first_name': 'First',
                'last_name': 'Last',
                'image_url': "",
            }
            resp = c.post('/users/new', data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("First", html)

    def test_show_user_profile(self):
        """ Test that user_profile renders """
        with self.client as c:

            resp = c.get(f'/users/{self.user_id}')
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("test_first", html)
            self.assertIn('Delete', html)

            resp = c.get(f'/users/1000')  # good/bad tests
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 404)

    def test_update_user_profile(self):
        """ Testing that edits to user profile processes correctly"""
        with self.client as c:
            resp = c.post(
                f'/users/{self.user_id}/edit',
                data={
                    "first_name": "update_first",
                    "last_name": "update_last",
                    "image_url": ""
                },
                follow_redirects=True
            )
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("update_first", html)

    def test_delete_user_profile(self):
        """ Test that user gets deleted from user list / table """
        with self.client as c:
            resp = c.post(
                f'/users/{self.user_id}/delete',
                follow_redirects=True
            )

            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("User has been deleted!", html)
            self.assertNotIn('test_first ', html)
            self.assertIn('test_last_two', html)


class PostViewTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""

        # As you add more models later in the exercise, you'll want to delete
        # all of their records before each test just as we're doing with the
        # User model below.
        Post.query.delete()
        User.query.delete()

        self.client = app.test_client()

        test_user = User(
            first_name="test_first",
            last_name="test_last",
            image_url=None,
        )

        second_user = User(
            first_name="test_first_two",
            last_name="test_last_two",
            image_url=None,
        )

        db.session.add_all([test_user, second_user])
        db.session.commit()

        # We can hold onto our test_user's id by attaching it to self (which is
        # accessible throughout this test class). This way, we'll be able to
        # rely on this user in our tests without needing to know the numeric
        # value of their id, since it will change each time our tests are run.
        self.user_id = test_user.id

        test_user_post = Post(
            title='Post for Test User',
            content='Content for test user.',
            user_id=self.user_id
        )

        db.session.add_all([test_user_post])
        db.session.commit()

        self.post_id = test_user_post.id

    def test_adding_new_post(self):
        """ tests adding new post"""
        with self.client as c:
            resp = c.post(
                f'/users/{self.user_id}/posts/new',
                data={'title': 'New Post',
                      'content': 'Post content'
                      },
                follow_redirects=True
            )
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('New Post', html)

    def test_new_post_invalid_data(self):
        """ tests adding new post"""
        with self.client as c:
            resp = c.post(
                f'/users/1000/posts/new',  # INVALID USER
                data={'title': 'New Post',
                      'content': 'Post content'
                      },
                follow_redirects=True
            )
            self.assertEqual(resp.status_code, 404)

        with self.client as c:
            resp = c.post(
                f'/users/{self.user_id}/posts/new',
                data={'title': '',  # MISSING TITLE
                      'content': 'Post content'
                      },
                follow_redirects=True
            )
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('ERROR', html)

        with self.client as c:
            resp = c.post(
                f'/users/{self.user_id}/posts/new',
                data={'title': '',  # MISSING TITLE
                      'content': ''  # MISSING CONTENT
                      },
                follow_redirects=True
            )
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('ERROR', html)

        with self.client as c:
            resp = c.post(
                f'/users/{self.user_id}/posts/new',
                data={'title': 'Title',
                      'content': ''  # MISSING CONTENT
                      },
                follow_redirects=True
            )
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('ERROR', html)

    def test_edit_post(self):
        """ tests editing post"""
        with self.client as c:
            resp = c.post(
                f'/posts/{self.post_id}/edit',
                data={'title': 'New Post - Edit',
                      'content': 'Post content - Edit'
                      },
                follow_redirects=True
            )
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('New Post - Edit', html)
            self.assertIn('Post content - Edit', html)

    def test_edit_post_invalid_data(self):
        """ tests adding new post"""
        with self.client as c:
            resp = c.post(
                f'/posts/1000/edit',
                data={'title': 'New Post',
                      'content': 'Post content'
                      },
                follow_redirects=True
            )
            self.assertEqual(resp.status_code, 404)

        with self.client as c:
            resp = c.post(
                f'/posts/{self.post_id}/edit',
                data={'title': '',
                      'content': 'Post content'
                      },
                follow_redirects=True
            )
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('ERROR', html)

        with self.client as c:
            resp = c.post(
                f'/posts/{self.post_id}/edit',
                data={'title': '',
                      'content': ''
                      },
                follow_redirects=True
            )
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('ERROR', html)

        with self.client as c:
            resp = c.post(
                f'/posts/{self.post_id}/edit',
                data={'title': 'Title',
                      'content': ''
                      },
                follow_redirects=True
            )
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('ERROR', html)

    def test_delete_post(self):
        """ Test that user gets deleted from user list / table """
        with self.client as c:
            resp = c.post(
                f'/posts/{self.post_id}/delete',
                follow_redirects=True
            )

            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Post has been deleted!", html)
            self.assertNotIn('Post for Test User', html)
