from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from schemas.users import UserCreate
from db.scripts.users import create_new_user, select_user_email
from jose import jwt
from jose import JWTError
from datetime import timedelta
from db.base import Users
from utils.auth import OAuth2PasswordBearerWithCookie
from utils.security import Hasher, create_access_token
from schemas.token import Token
from config import config

router = APIRouter()


def authenticate_user(username: str, password: str):
    user = select_user_email(username)
    print(user)
    if not user:
        return False
    if not Hasher.verify_password(password, user.password):
        return False
    return user


@router.post("/login", response_model=Token)
def login_for_access_token(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "role": user.role_id},
        expires_delta=access_token_expires,
    )
    response.set_cookie(
        key="access_token", value=f"Bearer {access_token}", httponly=True
    )
    return {"access_token": access_token, "token_type": "bearer"}


oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="/api/auth/login")


def get_current_user_from_token(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Неудается авторизировать",
    )
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = select_user_email(email=username)
    if user is None:
        raise credentials_exception
    return user


"""
@router.post("/")
def create_user(user: UserCreate):
    create_new_user(user.email, user.password)
    return {"result": "OK"}

"""
