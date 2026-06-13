import os
import uuid
from pydantic import BaseModel, Field

super_secret = b'super_secret_mock_key'

class loginInput(BaseModel):
    email: str = Field(..., description="Email address")
    password: str = Field(..., description="Password")

class signupInput(BaseModel):
    email: str = Field(..., description="Email address")
    password: str = Field(..., description="Password")
    confirm_password: str = Field(..., description="Confirm password")

class forgetPasswordInput(BaseModel):
    email: str = Field(..., description="Email address")

def display_error(e):
    return {"success": False, "error": str(e)}

def signup(email, pwd):
    return {"success": True, "user": {"localId": str(uuid.uuid4()), "idToken": "mock-token"}}

def login(email, pwd):
    return {"success": True, "user": {"localId": str(uuid.uuid4()), "idToken": "mock-token"}}

def forget_password(email):
    return {"success": True}

def logout():
    return {"success": True}

def send_verification_email(id_token):
    return {"success": True}

def is_email_verified(id_token):
    return {"success": True, "verified": True}

def delete_account(id_token):
    return {"success": True}