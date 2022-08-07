from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from config.config import Settings as Config
from dependencies import config
from dependencies.auth import get_current_user_authorizer
from models.user import User
from services import messenger

router = APIRouter(
    tags=["logout"],
)


class LogoutRequest(BaseModel):
    email: str
    password: str


class LogoutResponse(BaseModel):
    status: str


@router.post(
    '/logout',
    response_model=LogoutResponse,
    responses={
        401: {"detail": {"msg": "Not authorized"}}
    }
)
def logout(
        user: User = Depends(get_current_user_authorizer()),
        config: Config = Depends(config.get_config)
) -> LogoutResponse:
    try:
        client = messenger.get_client(user.email, user.password, config.user_agent.get_secret_value()
                                      , cookies=user.cookies)
        client.logout()
        return LogoutResponse(
            status="Ok"
        )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Can't logout")
