"""
Handles the login, logout, and token verification
"""

from pydantic import BaseModel
from fastapi import Header, HTTPException


class LoginData(BaseModel):
    """
    Username and password for logging in
    """

    username: str
    password: str


USERNAME = "username"
PASSWORD = "password"
TOKEN = "this-is-a-secret-token"


def verify_user(login_token: str = Header(...)):
    """
    Verify the user by checking the login token
    """
    if login_token != TOKEN:
        raise HTTPException(status_code=401, detail="Who are you?")


def login_user(request: LoginData):
    """
    When password and username is correct, return a login token
    """
    if request.username == USERNAME and request.password == PASSWORD:
        return {"success": True, "token": TOKEN}
    return {"success": False, "token": ""}


def logout_user():
    """
    When logging out, return a success message,
    doesn't actually do anything right now
    """
    return {"success": True, "message": "Successfully logged out"}
