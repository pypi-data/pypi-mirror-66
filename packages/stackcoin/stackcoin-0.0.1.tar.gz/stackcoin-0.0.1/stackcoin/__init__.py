from typing import Dict, Optional

from pydantic import BaseModel
import requests
from requests.exceptions import RequestException

from .exceptions import *


class TransferSuccess(BaseModel):
    message: str
    from_bal: int
    to_bal: int


class User(BaseModel):
    id: str
    bal: int


class Users(BaseModel):
    __root__: Dict[str, User]


class StackCoin:
    def __init__(self, *, base_url="https://stackcoin.world", token, user_id):
        self.base_url = base_url
        self.token = token
        self.user_id = user_id
        self._access_token = None

        self._access_token = self._authenticate()

    def _request(self, http_verb, path_postfix, *, json=None, should_retry=True):
        headers = {}
        if self._access_token is not None:
            headers["X-Access-Token"] = self._access_token

        while True:
            resp = requests.request(
                http_verb, f"{self.base_url}/{path_postfix}", headers=headers, json=json
            )

            if resp.status_code == 401:
                if not should_retry:
                    raise UnexpectedState(resp.text)

                self._access_token = self._authenticate()
                headers["X-Access-Token"] = self._access_token

                should_retry = False
            else:
                break

        try:
            resp_json = resp.json()
            if "error" in resp_json:
                if "message" in resp_json:
                    message = resp_json["message"]

                external_exception = type(resp_json["error"], (StackCoinException,), {})
                raise external_exception(message)
        except ValueError as e:
            raise UnexpectedState(e)

        try:
            resp.raise_for_status()
        except RequestException as e:
            raise RequestError(f"{e}: {resp.text}")

        return resp_json

    def _authenticate(self):
        try:
            resp_json = self._request(
                "POST",
                "auth",
                json={"token": self.token, "user_id": self.user_id},
                should_retry=False,
            )
        except RequestError as e:
            raise AuthenticationFailure(e)
        except UnexpectedState as e:
            raise AuthenticationFailure(e)

        if "access_token" in resp_json:
            return resp_json["access_token"]
        else:
            raise UnexpectedState(resp_json)

    def users(self) -> Dict[str, User]:
        try:
            return Users(__root__=self._request("GET", "user/")).__root__
        except RequestError:
            raise UnexpectedState(e)

    def user(self, user_id=None) -> Optional[User]:
        if user_id is None:
            user_id = self.user_id

        try:
            return User(**self._request("GET", f"user/{user_id}"))
        except RequestError:
            return None

    def transfer(self, to_id, amount) -> TransferSuccess:
        try:
            return TransferSuccess(
                **self._request(
                    "POST", "ledger/", json={"to_id": to_id, "amount": amount}
                )
            )
        except RequestError as e:
            raise TransferFailure(e)
