import unittest

from app.main import get_users_userid_transactions, post_users, get_users_userid, get_users_userid_points, post_users_userid_transactions, post_users_userid_points
from app.spend_request import SpendRequest
from app.transaction import Transaction
import uuid


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
        self.assertTrue(response)

    def test_get_users_userid_points_returns_proper_object(self):
        response = post_users()
        user_id = response.user_id
        response2 = get_users_userid_points(user_id)
        self.assertEqual('defaultdict', response2.__class__.__name__)
        self.assertIsNotNone(response.payer_points)
        self.assertIsNotNone(response.transactions)

    # transactions tests

    def test_post_users_transactions_has_all_attributes(self):
        response = post_users()
        user_id = response.user_id

        transaction = Transaction(
            payer='foo corp',
            points=100,
            timestamp='2022-05-05T05:05:05Z'
        )
        post_users_userid_transactions(user_id, transaction)

        response2 = get_users_userid_transactions(user_id)
        transaction = response2[0]

        self.assertEqual('foo corp', transaction.payer)
        self.assertEqual(100, transaction.points)
        self.assertEqual(
            '2022-05-05T05:05:05Z',
            transaction.timestamp
        )

    def test_post_users_transactions_has_payer_points(self):
        response = post_users()
        user_id = response.user_id

        transaction = Transaction(
            payer='foo corp',
            points=100,
            timestamp='2022-05-05T05:05:05Z'
        )
        post_users_userid_transactions(user_id, transaction)

        response2 = get_users_userid_points(user_id)
        all_payer_points = response2
        payer_points = all_payer_points['foo corp']

        self.assertEqual(100, payer_points)

    def test_post_users_transactions_sums_points_multiple_transactions(self):
        response = post_users()
        user_id = response.user_id

        transaction = Transaction(
            payer='foo corp',
            points=100,
            timestamp='2022-05-05T05:05:05Z'
        )
        post_users_userid_transactions(user_id, transaction)
        post_users_userid_transactions(user_id, transaction)

        response2 = get_users_userid_points(user_id)
        all_payer_points = response2
        payer_points = all_payer_points['foo corp']

        self.assertEqual(200, payer_points)

    def test_post_users_transactions_basic_negative_transaction(self):
        response = post_users()
        user_id = response.user_id

        transaction = Transaction(
            payer='foo corp',
            points=100,
            timestamp='2022-05-05T05:05:05Z'
        )
        post_users_userid_transactions(user_id, transaction)
        transaction = Transaction(
            payer='foo corp',
            points=-100,
            timestamp='2022-05-05T05:05:06Z'  # later
        )
        post_users_userid_transactions(user_id, transaction)

        response2 = get_users_userid_points(user_id)
        all_payer_points = response2
        payer_points = all_payer_points['foo corp']
        self.assertEqual(0, payer_points)

        response3 = get_users_userid_transactions(user_id)
        all_transactions = response2
        self.assertEqual(0, len(all_transactions))

    def test_post_users_transactions_reject_negative_trans_if_low_points(self):
        response = post_users()
        user_id = response.user_id

        transaction = Transaction(
            payer='foo corp',
            points=100,
            timestamp='2022-05-05T05:05:05Z'
        )
        post_users_userid_transactions(user_id, transaction)
        transaction = Transaction(
            payer='foo corp',
            points=-200,
            timestamp='2022-05-05T05:05:06Z'  # later
        )

        with self.assertRaises(Exception) as context:
            post_users_userid_transactions(user_id, transaction)
        ex = context.exception
        self.assertEqual(400, ex.status_code)
        self.assertEqual(
            'negative transaction aborted: not enough points available',
            ex.detail
        )

    # spend tests

    def test_post_users_userid_points_simple_spend_all(self):
        response = post_users()
        user_id = response.user_id

        transaction = Transaction(
            payer='foo corp',
            points=100,
            timestamp='2022-05-05T05:05:05Z'
        )
        post_users_userid_transactions(user_id, transaction)

        response2 = get_users_userid_points(user_id)
        all_payer_points = response2
        payer_points = all_payer_points['foo corp']
        self.assertEqual(100, payer_points)

        spend_request = SpendRequest(points=100)
        post_users_userid_points(user_id, spend_request)

        response3 = get_users_userid_points(user_id)
        all_payer_points = response3
        payer_points = all_payer_points['foo corp']
        self.assertEqual(0, payer_points)

    def test_post_users_userid_points_only_spend_1_of_2_payers(self):
        response = post_users()
        user_id = response.user_id

        transaction = Transaction(
            payer='foo corp',
            points=100,
            timestamp='2022-05-05T05:05:05Z'
        )
        post_users_userid_transactions(user_id, transaction)
        transaction = Transaction(
            payer='bar corp',
            points=200,
            timestamp='2022-05-05T05:05:06Z'  # later
        )
        post_users_userid_transactions(user_id, transaction)

        response2 = get_users_userid_points(user_id)
        all_payer_points = response2
        payer_points = all_payer_points['foo corp']
        self.assertEqual(100, payer_points)

        spend_request = SpendRequest(points=100)
        post_users_userid_points(user_id, spend_request)

        response3 = get_users_userid_points(user_id)
        all_payer_points = response3
        payer_points1 = all_payer_points['foo corp']
        self.assertEqual(0, payer_points1)
        payer_points2 = all_payer_points['bar corp']
        self.assertEqual(200, payer_points2)

    def test_post_users_userid_points_partial_spend_one_payer(self):
        response = post_users()
        user_id = response.user_id

        transaction = Transaction(
            payer='foo corp',
            points=100,
            timestamp='2022-05-05T05:05:05Z'
        )
        post_users_userid_transactions(user_id, transaction)

        response2 = get_users_userid_points(user_id)
        all_payer_points = response2
        payer_points = all_payer_points['foo corp']
        self.assertEqual(100, payer_points)

        spend_request = SpendRequest(points=50)
        post_users_userid_points(user_id, spend_request)

        response3 = get_users_userid_points(user_id)
        all_payer_points = response3
        payer_points1 = all_payer_points['foo corp']
        self.assertEqual(50, payer_points1)

    def test_post_users_userid_points_response_body_has_output(self):
        response = post_users()
        user_id = response.user_id

        transaction = Transaction(
            payer='foo corp',
            points=100,
            timestamp='2022-05-05T05:05:05Z'
        )
        post_users_userid_transactions(user_id, transaction)

        response2 = get_users_userid_points(user_id)
        all_payer_points = response2
        payer_points = all_payer_points['foo corp']
        self.assertEqual(100, payer_points)

        spend_request = SpendRequest(points=100)
        response3 = post_users_userid_points(user_id, spend_request)
        self.assertEqual('foo corp', response3[0]['payer'])
        self.assertEqual(-100, response3[0]['points'])

    def test_post_users_userid_points_refuse_to_spend_overage(self):
        response = post_users()
        user_id = response.user_id

        transaction = Transaction(
            payer='foo corp',
            points=100,
            timestamp='2022-05-05T05:05:05Z'
        )
        post_users_userid_transactions(user_id, transaction)

        response2 = get_users_userid_points(user_id)
        all_payer_points = response2
        payer_points = all_payer_points['foo corp']
        self.assertEqual(100, payer_points)

        spend_request = SpendRequest(points=200)
        with self.assertRaises(Exception) as context:
            post_users_userid_points(user_id, spend_request)
        ex = context.exception
        self.assertEqual(400, ex.status_code)
        self.assertEqual(
            'spend aborted: not enough points available',
            ex.detail
        )

        response3 = get_users_userid_points(user_id)
        all_payer_points = response3
        payer_points = all_payer_points['foo corp']
        self.assertEqual(100, payer_points)

    def test_post_users_userid_points_full_spend_payer1_partial_2(self):
        response = post_users()
        user_id = response.user_id

        transaction = Transaction(
            payer='aaron corp',
            points=100,
            timestamp='2022-05-05T05:05:05Z'
        )
        post_users_userid_transactions(user_id, transaction)
        transaction = Transaction(
            payer='shaver corp',
            points=400,
            timestamp='2022-05-05T05:05:06Z'  # later
        )
        post_users_userid_transactions(user_id, transaction)

        spend_request = SpendRequest(points=150)
        response = post_users_userid_points(user_id, spend_request)

        response2 = get_users_userid_points(user_id)
        all_payer_points = response2
        self.assertEqual(0, all_payer_points['aaron corp'])
        self.assertEqual(350, all_payer_points['shaver corp'])

        for payer_spend in response:
            if payer_spend['payer'] == 'foo corp':
                self.assertEqual(-100, payer_spend['points'])
            elif payer_spend['payer'] == 'bar corp':
                self.assertEqual(-50, payer_spend['points'])

    def test_post_users_userid_points_spend_older_transaction_first(self):
        response = post_users()
        user_id = response.user_id

        transaction = Transaction(
            payer='shaver corp',
            points=100,
            timestamp='2022-05-05T05:05:06Z'  # later
        )
        post_users_userid_transactions(user_id, transaction)
        transaction = Transaction(
            payer='aaron corp',
            points=100,
            timestamp='2022-05-05T05:05:05Z'
        )
        post_users_userid_transactions(user_id, transaction)

        spend_request = SpendRequest(points=100)
        response = post_users_userid_points(user_id, spend_request)

        for payer_spend in response:
            self.assertEqual('aaron corp', payer_spend['payer'])

        response2 = get_users_userid_points(user_id)
        all_payer_points = response2
        self.assertEqual(0, all_payer_points['aaron corp'])
        self.assertEqual(100, all_payer_points['shaver corp'])