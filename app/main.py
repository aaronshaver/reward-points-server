#!/usr/bin/env python3

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root_get():
    return {"Hello": "World"}
