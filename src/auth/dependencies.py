from fastapi.security import HTTPBearer
from fastapi import Request, status, Depends
from fastapi.security.http import HTTPAuthorizationCredentials
from fastapi.exceptions import HTTPException
from .utils import decode_token
from src.db.redis import token_in_blocklist
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from .service import UserService
from typing import List, Any
from src.db.models import User

from src.errors import (
    InvalidToken,
    RefreshTokenRequired,
    AccessTokenRequired,
    InsufficientPermission,
    AccountNotVerified
)


user_service = UserService()


class TokenBearer(HTTPBearer):

    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)

        if not creds:
            raise InvalidToken()

        token = creds.credentials

        token_data = decode_token(token)

        # if not token_data:
        #  raise InvalidToken()
        # raise HTTPException(
        # status_code=status.HTTP_403_FORBIDDEN, detail={
        # "error":"This token is invalid or expired",
        # "resolution":"Please get a new token"

        if await token_in_blocklist(token_data["jti"]):
            raise InvalidToken()

        self.verify_token_data(token_data)

        return token_data  # can get access to user id and user detail

    # now got token alr need to check if it is valid
    def token_valid(self, token: str) -> bool:
        token_data = decode_token(token)
        return True if token_data is not None else False

    # above checks if valid tokens have been provided

    def verify_token_data(self, token_data):
        raise NotImplementedError("Please Override this method in child classes")


class AccessTokenBearer(TokenBearer):  # check if access token is provided????

    def verify_token_data(self, token_data: dict) -> None:
        if (
            token_data and token_data["refresh"]
        ):  # means if they accidentally give refresh token instead of access token, raise an error
            raise AccessTokenRequired()


class RefreshTokenBearer(TokenBearer):  # check if refresh token is being provided

    def verify_token_data(self, token_data: dict) -> None:
        if (
            token_data and not token_data["refresh"]
        ):  # means if they accidentally give refresh token instead of access token, raise an error
            raise RefreshTokenRequired()


async def get_current_user(
    token_details: dict = Depends(AccessTokenBearer()),
    session: AsyncSession = Depends(get_session),
):
    user_email = token_details["user"]["email"]

    user = await user_service.get_user_by_email(user_email, session)

    return user


class RoleChecker:
    def __init__(self, allowed_roles: List[str]) -> None:

        self.allowed_roles = allowed_roles

    def __call__(self, current_user: User = Depends(get_current_user)) -> Any:
        if not current_user.is_verified:
            raise AccountNotVerified()

        if current_user.role in self.allowed_roles:
            return True

        raise InsufficientPermission()
