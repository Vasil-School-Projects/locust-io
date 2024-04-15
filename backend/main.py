"""
A simple FastAPI application to demonstrate locust.io
"""

import time
import uvicorn
from fastapi import FastAPI, Depends
from login import LoginData, verify_user, login_user, logout_user

app = FastAPI()


@app.post("/login")
def login(request: LoginData):
    """
    When password and username is correct, return a login token
    """
    return login_user(request)


@app.post("/logout")
def logout():
    """
    When logging out, return a success message,
    doesn't actually do anything right now
    """
    return logout_user()


@app.get("/fast", dependencies=[Depends(verify_user)])
def fast():
    """
    A route that returns a response quickly
    """
    time.sleep(0.5)
    return {"message": "This is a fast route"}


@app.get("/slow", dependencies=[Depends(verify_user)])
def slow():
    """
    A route that returns a response slowly
    """
    time.sleep(3)
    return {"message": "This is a slow route"}


if __name__ == "__main__":
    uvicorn.run(app, reload=True)
