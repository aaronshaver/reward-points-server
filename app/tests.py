from http.client import HTTPException
import unittest

from app.main import get_users_new, get_users_userid, get_users_userid_points
from points import Points
import uuid


class Tests(unittest.TestCase):

    # users tests
    def test_post_users_new_has_uuid(self):
        response = get_users_new()
        self.assertEqual(36, len(str(response.user_id)))

    def test_get_users_userid_returns_user(self):
        response = get_users_new()
        user_id = response.user_id
        response2 = get_users_userid(str(user_id))
        self.assertEqual(user_id, response2.user_id)

    def test_get_users_userid_nonexistent_user_expect_404(self):
        user_id = uuid.uuid4()
        with self.assertRaises(Exception) as context:
            get_users_userid(str(user_id))
        ex = context.exception
        self.assertEqual(404, ex.status_code)
        self.assertEqual('user not found', ex.detail)

    def test_post_users_new_has_points_attribute(self):
        response = get_users_new()
        self.assertTrue(response.points)

    def test_get_users_userid_points_returns_points_object(self):
        response = get_users_new()
        user_id = response.user_id
        response2 = get_users_userid_points(str(user_id))
        self.assertEqual('Points', response2.__class__.__name__)
