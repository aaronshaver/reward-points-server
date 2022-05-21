import unittest

from app.main import get_users_new


class Tests(unittest.TestCase):

    # setup
    def setUp(self):
        pass

    # users tests
    def test_get_users_new_has_uuid(self):
        response = get_users_new()
        self.assertEqual(36, len(str(response.user_id)))
