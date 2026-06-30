from fastapi import FastAPI, HTTPException, status
from pathlib import Path
from functools import wraps
import datetime
import jwt
import os
try:
    from minimusic.config.userconfig import Config
    from minimusic.db.userdata import UserData
except ModuleNotFoundError:
    import sys

    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from minimusic.config.userconfig import Config
    from minimusic.db.userdata import UserData

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

def admin_required():

    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            if not "admin" in UserData.get_user_role["roles"]:
                return {"msg": "Only admins can do that!"}, 403

            return fn(*args, **kwargs)

        return decorator

    return wrapper

def create_jwt_token(subject: str. expires: datetime.timedelta. token_type: str) -> str:
    payload = {
        "sub": subject,
        "exp": expires,
        "token_type": token_type
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def refresh_acess_token(refresh_token: str):
    payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])

    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type for this operation."
        )

    username = payload.get("sub")
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token without usernama identification".
        )

    new_access_token = create_jwt_token(
            subject=username,
            expires_delta=datetime.timedelta(minutes=15),
            token_type="access"
        )
        
        return {"access_token": new_access_token, "token_type": "bearer"}
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Expired Refresh Token. Login again."
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token."
        )