"""
MiniMusic Server API
 
Explaining the server API: the desktop window (pywebview) loads this server's
pages directly, and the frontend JS calls these endpoints over fetch().
FastAPI is too good to create a "mini server", to run, we use uvicorn.
"""
 
from pathlib import Path as FilePath
 
from fastapi import FastAPI, HTTPException, Path, status
from fastapi.responses import HTMLResponse
 
try:
    from minimusic.config.serverenv import PORT
    from minimusic.db.login import get_user_from_db, register_user
except ModuleNotFoundError:
    import sys
 
    sys.path.insert(0, str(FilePath(__file__).resolve().parents[2]))
    from minimusic.config.serverenv import PORT
    from minimusic.db.login import get_user_from_db, register_user
 
from werkzeug.security import check_password_hash
from pydantic import BaseModel
import uvicorn
 
app = FastAPI()
 
 
class LoginRequest(BaseModel):
    username: str
    password: str
 
 
class RegisterRequest(BaseModel):
    username: str
    password: str
 
 

 
@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Mini Music | Welcome</title>
        <style>
            body {
                margin: 0;
                height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                background: #0a0a0d;
                color: #eeeef0;
                font-family: system-ui, -apple-system, BlinkMacSystemFont,
                    "Segoe UI", Roboto, Oxygen, Ubuntu, Cantarell,
                    "Open Sans", "Helvetica Neue", sans-serif;
            }
            .welcome-container {
                text-align: center;
            }
            .welcome-container h2 {
                font-size: 22px;
                font-weight: 600;
                margin-bottom: 20px;
            }
            .welcome-container button {
                background: #7C6FEB;
                color: #fff;
                border: none;
                border-radius: 8px;
                padding: 11px 24px;
                font-size: 14px;
                font-weight: 600;
                cursor: pointer;
            }
            .welcome-container button:hover {
                background: #5a4fcf;
            }
        </style>
    </head>
    <body>
        <div class="welcome-container">
            <h2>Welcome to Mini Music!</h2>
            <button onclick="window.location.href='/onboarding'">Let's start</button>
        </div>
    </body>
    </html>
    """
 
 
@app.get("/health")
async def health():
    return {"status": "online"}
 
 
@app.post("/login")
async def post_login(data: LoginRequest):
    user = get_user_from_db(data.username)
 
    if not user or not check_password_hash(user.password, data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password.",
        )
 
    
    return {"user_id": user.id, "username": user.username}
 
 
@app.post("/register", status_code=status.HTTP_201_CREATED)
async def post_register(data: RegisterRequest):
    if not data.username or not data.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username and password are required.",
        )
 
    if len(data.password) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 6 characters.",
        )
 
    
    user = register_user(data.username, data.password)
 
    if not user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already taken.",
        )
 
    return {"user_id": user.id, "username": user.username}
 
 

 
@app.get("/api/musics_get")
async def api_musics_get(music: str = ""):
    if not music:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No music path found! Select a folder for your music.",
        )
 
    # TODO: look up the actual indexed songs for this folder/user
    return {"path": music}
 
 
def runServer():
    uvicorn.run(app, port=PORT, host="0.0.0.0")
 
 
if __name__ == "__main__":
    runServer()
