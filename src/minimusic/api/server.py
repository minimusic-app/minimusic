"""
MiniMusic Server API

Explaining the server API, the PyQt6 App we will send requests for the server.
FastAPI is too good to create a "mini server", to run, we use uvicorn.
"""

from fastapi import FastAPI, HTTPException, status
from config.serverenv import PORT
from db.login import get_user_from_db
from werkzeug.security import check_password_hash
from pydantic import BaseModel
import uvicorn

app = FastAPI()

class LoginRequest(BaseModel):
    username: str
    password: str

app.get("/")
async def root():
    return {"status": "Online"}

def login_minimusic(username, password):
    payload = {"username": username, "password": password}

@app.post("/login")
async def post_login(data: LoginRequest):
    user = get_user_from_db(data.username)

    if not user or not check_password_hash(user.password, data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Password or Username"
        )
    
    return user

@app.post("/register")
async def post_register():
    user = register_user()

    if not user or not generate_password_hash(user):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No Password or Username."
    )
    else:
        raise HTTPException(
            status_code=status.HTTP_100_CONTINUE
        )

def runServer():
    uvicorn.run(app, port=PORT, host="0.0.0.0")


if __name__ == "__main__":
    runServer()
