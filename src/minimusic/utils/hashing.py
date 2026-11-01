import hashlib
from pathlib import Path

from werkzeug.security import check_password_hash, generate_password_hash


def hash_text(text: str, algorithm: str = "sha256") -> str:
    """Return the hexadecimal digest of text encoded as UTF-8."""
    digest = hashlib.new(algorithm)
    digest.update(text.encode("utf-8"))
    return digest.hexdigest()


def hash_username(username: str) -> str:
    """Return a stable hash for a username."""
    return hash_text(username)


def hash_password(password: str) -> str:
    """Hash a password using Werkzeug's salted password-hashing scheme."""
    return generate_password_hash(password)


def verify_password(password_hash: str, password: str) -> bool:
    """Check a password against a hash created by hash_password."""
    return check_password_hash(password_hash, password)


def hash_file(
    path: str | Path,
    algorithm: str = "sha256",
    chunk_size: int = 8192,
) -> str:
    """Return the hexadecimal digest of a file without loading it all into memory."""
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero")

    digest = hashlib.new(algorithm)
    with Path(path).open("rb") as file:
        for chunk in iter(lambda: file.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest()