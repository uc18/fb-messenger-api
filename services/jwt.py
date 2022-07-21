from datetime import datetime, timedelta
from typing import Dict

import jwt
from pydantic import ValidationError

from models.user import User

JWT_SUBJECT = "access"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # one week


def create_jwt_token(
    *,
    jwt_content: Dict[str, str],
    secret_key: str,
) -> str:
    to_encode = jwt_content.copy()
    to_encode.update()
    to_encode.update({"sub": JWT_SUBJECT})
    return jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)


def create_access_token_for_user(user: User, secret_key: str) -> str:
    return create_jwt_token(
        jwt_content=user.dict(),
        secret_key=secret_key,
    )


def get_user_from_token(token: str, secret_key: str) -> str:
    try:
        return User(**jwt.decode(token, secret_key, algorithms=[ALGORITHM]))
    except jwt.PyJWTError as decode_error:
        raise ValueError("unable to decode JWT token") from decode_error
    except ValidationError as validation_error:
        raise ValueError("malformed payload in token") from validation_error