from typing import List
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from dependencies.auth import get_current_user_authorizer
from dependencies import config
from config.config import Settings as Config

from models.user import User as DUser

from fbchat.models import *

from services import messenger


router = APIRouter(
    prefix="/contacts",
    tags=["contacts"],
)


class SendRequest(BaseModel):
    message: str
    thread_id: str


class SendResponse(BaseModel):
    msg_id: str


@router.post("/send")
def send(
    req: SendRequest,
    user: User = Depends(get_current_user_authorizer()),
    config: Config = Depends(config.get_config)
) -> SendResponse:
    client = messenger.get_client(user.email, user.password, config.user_agent.get_secret_value(), cookies=user.cookies)
    try:
        message = client.send(Message(text=req.message), thread_id=req.thread_id)
        return SendResponse(msg_id=message)
    except:
        raise HTTPException(status_code=422, detail={"msg": "not found thread"})
    

class SearchRequest(BaseModel):
    q: str
    limit: int = 10


@router.post("/search")
def search(
    req: SearchRequest,
    user: DUser = Depends(get_current_user_authorizer()),
    config: Config = Depends(config.get_config)
) -> List[User]:
    client = messenger.get_client(user.email, user.password, config.user_agent.get_secret_value(), cookies=user.cookies)

    users = client.searchForUsers(req.q, req.limit)
    return users


@router.get(
    "/messages/{contact}",
)
def messages_by_contact(
    contact,
    user: DUser = Depends(get_current_user_authorizer()),
    config: Config = Depends(config.get_config)
):
    try:
        client = messenger.get_client(user.email, user.password, config.user_agent.get_secret_value(), cookies=user.cookies)
        messages = client.fetchThreadMessages(contact)
    except ValueError:
        raise HTTPException(status_code=422, detail={"msg": "not found thread"})
    return messages
