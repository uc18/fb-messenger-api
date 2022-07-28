from http.client import responses
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from config.config import Settings as Config
from dependencies import config
from dependencies.auth import get_current_user_authorizer
from models.user import User
from services import messenger, jwt

router = APIRouter(
    tags=["login"],
)


class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    uid: str
    token: str


class CheckRequest(BaseModel):
    email: str


class CheckResponse(BaseModel):
    login: str
    isLoggedIn: bool


@router.post(
    '/login',
    response_model=LoginResponse,
    responses={
        401: {"detail": {"msg": "Not authorized"}}
    }    
)
def login(
    request: LoginRequest,
    config: Config = Depends(config.get_config)
) -> LoginResponse:
    try:
        client = messenger.get_client(request.email, request.password, config.user_agent.get_secret_value())
        user = User(email=request.email, password=request.password, cookies=client.getSession())
        token = jwt.create_access_token_for_user(user, config.jwt_secret.get_secret_value())
        
        return LoginResponse(
            uid=client.uid,
            token=token
        )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=401, detail="Not authorized")

@router.get(
    '/check',
    response_model=CheckResponse,
    responses={
        401: {"detail": {"msg": "Not authorized"}}
    }
)
def check(
        user: User = Depends(get_current_user_authorizer()),
        config: Config = Depends(config.get_config)
) -> CheckResponse:
    try:

        client = messenger.get_client(user.email, user.password, config.user_agent.get_secret_value(),
                                      cookies=user.cookies)

        logged = client.isLoggedIn()

        return CheckResponse(
            login=client.uid,
            isLoggedIn=logged
        )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=401, detail="Not authorized")
