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
        payer_name = transaction.payer_name
        users[user_id].points.transactions.append(transaction)

        existing_points_total = users[user_id].points.payer_points[payer_name]
        users[user_id].points.payer_points[payer_name] = existing_points_total \
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
    if user_id in users:
        total_points_available = sum(users[user_id].points.payer_points.values())
        if spend_request.points > total_points_available:
            raise HTTPException(
                status_code=400,
                detail="spend aborted: not enough points available"
            )

        transactions = users[user_id].points.transactions
        transaction1 = transactions[0]

        spent_amounts = {}
        payer_name = transaction1.payer_name
        spent_amounts[payer_name] = spend_request.points
        del transactions[0]
        existing_amount = users[user_id].points.payer_points[payer_name]
        users[user_id].points.payer_points[payer_name] -= spend_request.points
    else:
        raise HTTPException(
            status_code=404,
            detail="user not found"
        )