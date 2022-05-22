#!/usr/bin/env python3

from fastapi import FastAPI, HTTPException

from app.points import Points
from .user import User
from .transaction import Transaction


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
        users[user_id].points.transactions[payer_name].append(transaction)
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
    -probably will not be used in the app itself; however, useful for Postman
    manual testing
    """
    if user_id in users:
        return users[user_id].points.transactions
    else:
        raise HTTPException(
            status_code=404,
            detail="user not found"
        )
