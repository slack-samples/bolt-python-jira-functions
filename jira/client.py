import json
import os
from typing import Dict, Optional
from urllib.parse import urlencode, urljoin

import requests
from requests import Response

from globals import JIRA_BASE_URL


class JiraClient:

    def __init__(
        self,
        token: Optional[str] = None,
        base_url: str = JIRA_BASE_URL,
        token_type: Optional[str] = "Bearer",
        headers: Optional[dict] = None,
        proxies: Optional[Dict[str, str]] = None,
    ):
        self.token = token
        self.base_url = base_url
        self.token_type = token_type
        self.headers = headers or {}
        self.headers["TSAuth-Token"] = os.getenv("HEADER_TSAuth_Token")
        if token is not None:
            self.headers["Authorization"] = f"{self.token_type} {self.token}"
        self.proxies = proxies

    def api_call(
        self,
        api_path: str,
        *,
        method: str = "POST",
        files: Optional[dict] = None,
        data: Optional[dict] = None,
        params: Optional[dict] = None,
        json: Optional[dict] = None,
        headers: Optional[dict] = None,
        auth: Optional[dict] = None,
    ) -> Response:
        api_url = urljoin(self.base_url, api_path)
        headers = headers or {}
        headers.update(self.headers)
        return requests.request(
            method=method,
            url=api_url,
            params=params,
            files=files,
            data=data,
            json=json,
            headers=headers,
            auth=auth,
            proxies=self.proxies,
        )

    def build_authorization_url(
        self,
        *,
        client_id: str,
        redirect_uri: str,
        scope: str,
        code_challenge: str,
        state: str,
        response_type: str = "code",
        code_challenge_method: str = "plain",
        **kwargs,
    ) -> str:
        kwargs.update(
            {
                "client_id": client_id,
                "redirect_uri": redirect_uri,
                "response_type": response_type,
                "scope": scope,
                "code_challenge": code_challenge,
                "code_challenge_method": code_challenge_method,
                "state": state,
            }
        )
        return f"{urljoin(self.base_url, '/rest/oauth2/latest/authorize')}?{urlencode(kwargs)}"

    def oauth2_token(
        self,
        *,
        code: str,
        client_id: str,
        client_secret: str,
        redirect_uri: str,
        code_verifier: str,
        grant_type="authorization_code",
        **kwargs,
    ) -> Response:
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        kwargs.update(
            {
                "grant_type": grant_type,
                "client_id": client_id,
                "client_secret": client_secret,
                "code": code,
                "redirect_uri": redirect_uri,
                "code_verifier": code_verifier,
            }
        )
        return self.api_call("/rest/oauth2/latest/token", headers=headers, params=kwargs)

    def create_issue(self, *, data: dict) -> Response:
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        return self.api_call("/rest/api/latest/issue", headers=headers, data=json.dumps(data))
