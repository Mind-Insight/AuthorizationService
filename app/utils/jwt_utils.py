from datetime import datetime, timedelta
import bcrypt
import jwt

from core.config import auth_jwt


def encode_jwt(
    payload: dict,
    private_key: str = auth_jwt.private_key_path.read_text(),
    algorithm: str = auth_jwt.algorithm,
    expire_time_delta: timedelta | None = None,
    expire_minutes: int = auth_jwt.access_token_expire_minutes,
):
    to_encode = payload.copy()
    now = datetime.utcnow()
    if expire_time_delta:
        expire = now + timedelta()
    else:
        expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(exp=expire, iat=now)
    encoded = jwt.encode(to_encode, private_key, algorithm=algorithm)
    return encoded


def decode_jwt(
    token: str | None,
    public_key: str = auth_jwt.public_key_path.read_text(),
    algorithm: str = auth_jwt.algorithm,
):
    decoded = jwt.decode(token, public_key, algorithms=[algorithm])
    return decoded


def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)


def validate_password(password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(
        password.encode(), hashed_password=hashed_password
    )
