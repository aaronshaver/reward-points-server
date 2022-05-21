#!/usr/bin/env python3

from fastapi import FastAPI
from .user import User

app = FastAPI()


@app.post("/users/new", status_code=201)
def get_users_new():
    """
    -Creates and returns a new User
    -POST because operation creates a resource, is not idempotent
    """
    return User()
