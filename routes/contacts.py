from typing import List
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from dependencies.auth import get_current_user_authorizer

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
) -> SendResponse:
    client = messenger.get_client(user.email, user.password, user.cookies)
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
) -> List[User]:
    client = messenger.get_client(user.email, user.password, user.cookies)

    users = client.searchForUsers(req.q, req.limit)
    return users

@router.get(
    "/messages/{contact}",
)
def messages_by_contact(
    contact,
    user: DUser = Depends(get_current_user_authorizer()),
):
    try:
        client = messenger.get_client(user.email, user.password, user.cookies)
        messages = client.fetchThreadMessages(contact)
        return messages
    except:
        raise HTTPException(status_code=422, detail={"msg": "not found thread"})
    