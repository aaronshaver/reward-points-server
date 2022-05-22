#!/usr/bin/env python3

from fastapi import FastAPI, HTTPException

from app.points import Points
from .user import User
import json

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

@app.post("/users/{user_id}/transactions", status_code=200)
def post_users_userid_transactions(user_id: str, transaction: str):
    """
    -accepts JSON body transaction and creates transaction resources in the
    system
    """
    if user_id in users:
        parsed_transaction = json.loads(transaction)
        payer_name = parsed_transaction['payer_name']
        points = parsed_transaction['points']
        timestamp = parsed_transaction['timestamp']
        transaction = {}
        transaction['payer_name'] = payer_name
        transaction['points'] = points
        transaction['timestamp'] = timestamp
        users[user_id].points.transactions[payer_name].append(transaction)
    else:
        raise HTTPException(
            status_code=404,
            detail="user not found"
        )
