from typing import Optional, Callable
from fastapi import Depends, HTTPException, Security
from fastapi.security import APIKeyHeader
from starlette import requests, status
from starlette.exceptions import HTTPException as StarletteHTTPException
from config.config import Settings as Config
from dependencies import config

from models.user import User
from services import jwt


HEADER_KEY = "Authorization"


class RWAPIKeyHeader(APIKeyHeader):
    async def __call__(  # noqa: WPS610
        self,
        request: requests.Request,
    ) -> Optional[str]:
        try:
            return await super().__call__(request)
        except StarletteHTTPException as original_auth_exc:
            raise HTTPException(
                status_code=original_auth_exc.status_code,
                detail={"msg": "AUTHENTICATION_REQUIRED"},
            )


def get_current_user_authorizer(*, required: bool = True) -> Callable:  # type: ignore
    return _get_current_user if required else _get_current_user_optional


def _get_authorization_header_retriever(
    *,
    required: bool = True,
) -> Callable:  # type: ignore
    return _get_authorization_header if required else _get_authorization_header_optional


def _get_authorization_header(
    api_key: str = Security(RWAPIKeyHeader(name=HEADER_KEY)),
) -> str:
        try:
            token_prefix, token = api_key.split(" ")
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"msg": "WRONG_TOKEN_PREFIX"},
            )
        if token_prefix != "Bearer":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"msg": "WRONG_TOKEN_PREFIX"},
            )
        return token


def _get_authorization_header_optional(
    authorization: Optional[str] = Security(
        RWAPIKeyHeader(name=HEADER_KEY, auto_error=False),
    ),
) -> str:
    if authorization:
        return _get_authorization_header(authorization)

    return ""


def _get_current_user(
    token: str = Depends(_get_authorization_header_retriever()),
    config: Config = Depends(config.get_config)
) -> User:
    try:
        return jwt.get_user_from_token(
            token,
            config.jwt_secret.get_secret_value(),
        )
    except SystemError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"msg": "TOKEN_EXPIRED"}
        )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"msg": "MALFORMED_PAYLOAD"},
        )


def _get_current_user_optional(
    token: str = Depends(_get_authorization_header_retriever(required=False)),
) -> Optional[User]:
    if token:
        return _get_current_user(token)

    return None
