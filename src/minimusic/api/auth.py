import datetime
import os

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from ..db.userdata import UserData

ALGORITHM = "HS256"
ACCESS_TOKEN_LIFETIME = datetime.timedelta(minutes=15)
_bearer_scheme = HTTPBearer(auto_error=False)


def _get_secret_key() -> str:
    secret_key = os.getenv("SECRET_KEY")
    if not secret_key:
        raise RuntimeError("SECRET_KEY must be configured to use authentication.")
    return secret_key


def create_jwt_token(
    subject: str,
    expires_delta: datetime.timedelta = ACCESS_TOKEN_LIFETIME,
    token_type: str = "access",
) -> str:
    if not subject:
        raise ValueError("subject must not be empty")
    if expires_delta <= datetime.timedelta(0):
        raise ValueError("expires_delta must be greater than zero")
    if token_type not in {"access", "refresh"}:
        raise ValueError("token_type must be 'access' or 'refresh'")

    expires_at = datetime.datetime.now(datetime.timezone.utc) + expires_delta
    payload = {
        "sub": subject,
        "exp": expires_at,
        "token_type": token_type,
    }
    return jwt.encode(payload, _get_secret_key(), algorithm=ALGORITHM)


def _decode_jwt_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, _get_secret_key(), algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired. Please log in again.",
            headers={"WWW-Authenticate": "Bearer"},
        ) from error
    except jwt.InvalidTokenError as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token.",
            headers={"WWW-Authenticate": "Bearer"},
        ) from error

    if not isinstance(payload, dict):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return payload


def refresh_access_token(refresh_token: str) -> dict[str, str]:
    payload = _decode_jwt_token(refresh_token)
    if payload.get("token_type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="A refresh token is required.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    username = payload.get("sub")
    if not isinstance(username, str) or not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token does not identify a user.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_jwt_token(username)
    return {"access_token": access_token, "token_type": "bearer"}


def refresh_acess_token(refresh_token: str) -> dict[str, str]:
    """Compatibility alias; use refresh_access_token instead."""
    return refresh_access_token(refresh_token)


def admin_required(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer_scheme),
) -> str:
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication is required.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    payload = _decode_jwt_token(credentials.credentials)
    username = payload.get("sub")
    if payload.get("token_type") != "access" or not isinstance(username, str) or not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="A valid access token is required.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if UserData.get_user_role(username) != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can do that!",
        )
    return username
