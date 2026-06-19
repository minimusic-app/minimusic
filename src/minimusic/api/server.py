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


@app.get("login", response_class=HTMLResponse)
async def login_page():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Mini Music | Sign in</title>
    
    <style>
            * { box-sizing: border-box; }
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
            .card {
                width: 320px;
                background: #18181c;
                border: 1px solid #2a2a35;
                border-radius: 16px;
                padding: 32px 28px 24px;
            }
            .card h2 {
                margin: 0 0 4px;
                font-size: 20px;
                font-weight: 700;
                text-align: center;
            }
            .card .subtitle {
                margin: 0 0 20px;
                font-size: 13px;
                color: #8888a0;
                text-align: center;
            }
            label {
                display: block;
                font-size: 11px;
                font-weight: 600;
                letter-spacing: 0.5px;
                color: #8888a0;
                margin-bottom: 4px;
            }
            input {
                width: 100%;
                background: #0e0e11;
                border: 1px solid #2a2a35;
                border-radius: 8px;
                padding: 10px 12px;
                color: #eeeef0;
                font-size: 13px;
                margin-bottom: 14px;
            }
            input:focus {
                outline: none;
                border-color: #7C6FEB;
            }
            button {
                width: 100%;
                background: #7C6FEB;
                color: #fff;
                border: none;
                border-radius: 8px;
                padding: 11px;
                font-size: 13px;
                font-weight: 600;
                cursor: pointer;
            }
            button:hover { background: #5a4fcf; }
            button:disabled { background: #2a2a35; color: #8888a0; cursor: default; }
            .error {
                color: #e05c5c;
                font-size: 12px;
                text-align: center;
                margin: 10px 0 0;
                min-height: 16px;
            }
            .switch {
                text-align: center;
                margin-top: 16px;
            }
            .switch a {
                color: #7C6FEB;
                font-size: 12px;
                text-decoration: none;
            }
            .switch a:hover { color: #eeeef0; }
        </style>
    </head>
    <body>
        <div class="card"> 
            <h2>Welcome Back</h2>
            <p class="subtitle">Sign In your Mini Music</p>

            <form id="login-form">
                <label for="username">Username</label>
                <input id="username" name="username" type="text" autocomplete="username" required>
 
                    <label for="password">Password</label>
                    <input id="password" name="password" type="password" autocomplete="current-password" required>
                
                    <button id="submit-btn" type="submit">Sign in</button>
                    <p id="error" class="error"></p>
            </form>

            <div class="switch">
                <a href="/register">Don't have an account? Create one</a>
            </div>
        </div>

        <script>
                const form = document.getElementById("login-form");
                const btn = document.getElementById("submit-btn");
                const errorEl = document.getElementById("error");
 
                form.addEventListener("submit", async (e) => {
                    e.preventDefault();
                    errorEl.textContent = "";
                    btn.disabled = true;
                    btn.textContent = "Signing in…";
 
                    const username = document.getElementById("username").value.trim();
                    const password = document.getElementById("password").value;
 
                    try {
                        const res = await fetch("/login", {
                            method: "POST",
                            headers: { "Content-Type": "application/json" },
                            body: JSON.stringify({ username, password }),
                        });
                        const data = await res.json();
 
                        if (!res.ok) {
                            throw new Error(data.detail || "Login failed.");
                        }
 
                        localStorage.setItem("minimusic_user_id", data.user_id);
                        localStorage.setItem("minimusic_username", data.username);
                        window.location.href = "/";
                    } catch (err) {
                        errorEl.textContent = err.message;
                        btn.disabled = false;
                        btn.textContent = "Sign in";
                    }
                });
            </script>
    """
 
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
