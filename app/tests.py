from http.client import HTTPException
import unittest

from app.main import users, post_users, get_users_userid, get_users_userid_points, post_users_userid_transactions
from app.transaction import Transaction
from points import Points
import uuid
import json


class Tests(unittest.TestCase):

    # users tests

    def test_post_users_has_uuid(self):
        response = post_users()
        self.assertEqual(36, len(response.user_id))

    def test_get_users_userid_returns_user(self):
        response = post_users()
        user_id = response.user_id
        response2 = get_users_userid(user_id)
        self.assertEqual(user_id, response2.user_id)

    def test_get_users_userid_nonexistent_user_expect_404(self):
        user_id = uuid.uuid4()
        with self.assertRaises(Exception) as context:
            get_users_userid(user_id)
        ex = context.exception
        self.assertEqual(404, ex.status_code)
        self.assertEqual('user not found', ex.detail)

    def test_post_users_has_points_attribute(self):
        response = post_users()
        self.assertTrue(response.points)

    def test_get_users_userid_points_returns_points_object(self):
        response = post_users()
        user_id = response.user_id
        response2 = get_users_userid_points(user_id)
        self.assertEqual('Points', response2.__class__.__name__)

    # transactions tests

    def test_post_users_transactions_has_all_attributes(self):
        response = post_users()
        user_id = response.user_id

        transaction = Transaction(
            payer_name='foo corp',
            points=100,
            timestamp='2022-05-05T05:05:05Z'
        )
        post_users_userid_transactions(user_id, transaction)

        response2 = get_users_userid_points(user_id)
        all_transactions = response2.transactions
        payer_transactions = all_transactions['foo corp']

        self.assertEqual(100, payer_transactions[0].points)
        self.assertEqual(
            '2022-05-05T05:05:05Z',
            payer_transactions[0].timestamp
        )

    def test_post_users_transactions_has_payer_points(self):
        response = post_users()
        user_id = response.user_id

        transaction = Transaction(
            payer_name='foo corp',
            points=100,
            timestamp='2022-05-05T05:05:05Z'
        )
        post_users_userid_transactions(user_id, transaction)

        response2 = get_users_userid_points(user_id)
        all_payer_points = response2.payer_points
        payer_points = all_payer_points['foo corp']

        self.assertEqual(100, payer_points)

    def test_post_users_transactions_sums_points_multiple_transactions(self):
        response = post_users()
        user_id = response.user_id

        transaction = Transaction(
            payer_name='foo corp',
            points=100,
            timestamp='2022-05-05T05:05:05Z'
        )
        post_users_userid_transactions(user_id, transaction)
        post_users_userid_transactions(user_id, transaction)

        response2 = get_users_userid_points(user_id)
        all_payer_points = response2.payer_points
        payer_points = all_payer_points['foo corp']

        self.assertEqual(200, payer_points)