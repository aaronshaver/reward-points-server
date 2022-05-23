#!/usr/bin/env python3

from re import U
from fastapi import FastAPI, HTTPException

from app.points import Points
from .user import User
from .transaction import Transaction
from .spend_request import SpendRequest


app = FastAPI()
users = {}


@app.post("/users", status_code=201)
def post_users():
    """
    -Creates and returns a new User
    -POST because operation creates a resource, is not idempotent
    """
    user = User()
    users[str(user.user_id)] = user
    return user

@app.get("/users/{user_id}", status_code=200)
def get_users_userid(user_id: str):
    """
    -returns a User matching the user ID on the path
    """
    if user_id in users:
        return users[user_id]
    else:
        raise HTTPException(
            status_code=404,
            detail="user not found"
        )

@app.get("/users/{user_id}/points", status_code=200)
def get_users_userid_points(user_id: str):
    """
    -returns a Points object for a given user_id
    """
    if user_id in users:
        return users[user_id].points
    else:
        raise HTTPException(
            status_code=404,
            detail="user not found"
        )

@app.post("/users/{user_id}/transactions", status_code=201)
def post_users_userid_transactions(user_id: str, transaction: Transaction):
    """
    -accepts JSON body transaction and creates transaction resources in the
    system
    """
    if user_id in users:
        payer = transaction.payer

        users[user_id].points.transactions.append(transaction)
        # sort in-place by timestamp asc. after adding the latest transaction
        users[user_id].points.transactions.sort(key=lambda x: x.timestamp)

        existing_points_total = users[user_id].points.payer_points[payer]
        users[user_id].points.payer_points[payer] = existing_points_total \
            + transaction.points

        return transaction
    else:
        raise HTTPException(
            status_code=404,
            detail="user not found"
        )

@app.get("/users/{user_id}/transactions", status_code=200)
def get_users_userid_transactions(user_id: str):
    """
    -returns transactions for a given user_id
    -not used in the app itself; however, useful for Postman manual testing
    """
    if user_id in users:
        return users[user_id].points.transactions
    else:
        raise HTTPException(
            status_code=404,
            detail="user not found"
        )

@app.post("/users/{user_id}/points", status_code=200)
def post_users_userid_points(user_id: str, spend_request: SpendRequest):
    """
    -spends the number of points requested for the user_id, if possible
    """
    # error handling
    if user_id not in users:
        raise HTTPException(
            status_code=404,
            detail="user not found"
        )
    if spend_request.points < 1:
        raise HTTPException(
            status_code=400,
            detail="unsupported points spending amount; please spend 1 point or more"
        )
    total_points_available = sum(users[user_id].points.payer_points.values())
    if spend_request.points > total_points_available:
        raise HTTPException(
            status_code=400,
            detail="spend aborted: not enough points available"
        )

    # core logic
    left_to_spend = spend_request.points
    transactions = users[user_id].points.transactions
    payer_spends = []
    transactions_to_delete = []
    for transaction in transactions:
        if left_to_spend == 0:
            break
        payer = transaction.payer
        transaction_amount_available = transaction.points
        # spend all points from this transaction
        if left_to_spend >= transaction_amount_available:
            spend_deduction = transaction_amount_available
            transactions_to_delete.append(transaction)
        # spend partial points, because trans. had more than we needed
        else:
            transaction.points -= left_to_spend
            spend_deduction = left_to_spend
        left_to_spend -= spend_deduction
        payer_spend = {}
        payer_spend['payer'] = payer
        payer_spend['points'] = spend_deduction * -1
        payer_spends.append(payer_spend)
    for transaction in transactions_to_delete:
        users[user_id].points.transactions.remove(transaction)

    spent_amounts = []
    for payer_spend in payer_spends:
        existing_payer = [x for x in spent_amounts if x['payer'] == \
            payer_spend['payer']]
        if existing_payer:
            existing_payer['points'] -= payer_spend['points']
        else:
            spent_amounts.append({'payer': payer_spend['payer'], \
                'points': payer_spend['points']})
        # subtract amount spent from a payer total for the user
        existing_amount = users[user_id].points.payer_points[payer_spend['payer']]
        users[user_id].points.payer_points[payer_spend['payer']] = \
            existing_amount + payer_spend['points']

    return spent_amounts