from datetime import datetime, timedelta

from fastapi import status, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext

from source.db import users, database
from source.models.token import TokenData
from source.models.user import BaseUser
from source.settings import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/sign-in/")


async def get_user(username: str):
    query = users.select().where(users.c.username == username)
    return await database.fetch_one(query)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def authenticate_user(username: str, password: str):
    user_record = await get_user(username)
    user = BaseUser.parse_obj(user_record)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict):
    to_encode = data.copy()
    now = datetime.utcnow()
    to_encode.update({'exp': now + timedelta(seconds=settings.jwt_expires_sec)})
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return BaseUser.parse_obj(user)


async def get_current_active_user(current_user: BaseUser = Depends(get_current_user)):
    if current_user.user_status == "Заблокирован":
        raise HTTPException(status_code=400, detail="User has been blocked")
    return current_user
