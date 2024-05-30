import json
import logging
from datetime import datetime
from unittest.mock import MagicMock, Mock, patch

import requests
from slack_sdk import WebClient

from listeners.functions.create_issue import create_issue_callback
from tests.utils import build_mock_context, remove_os_env_temporarily, restore_os_env


def mock_response(status=200, data: dict = None):
    mock_resp = MagicMock(status_code=status)
    if data:
        mock_resp.json = MagicMock(return_value=data)
        mock_resp.text = json.dumps(data)
    return mock_resp


class TestCreateIssue:
    user_id = "U1234"
    team_id = "T1234"
    enterprise_id = "E1234"

    def setup_method(self):
        self.old_os_env = remove_os_env_temporarily()
        self.mock_context = build_mock_context(team_id=self.team_id)
        self.mock_context.jira_installation_store.save(
            {
                "scope": "WRITE",
                "access_token": "jira_access_token",
                "token_type": "Bearer",
                "expires_in": 1000,
                "refresh_token": "jira_refresh_token",
                "user_id": self.user_id,
                "team_id": self.team_id,
                "enterprise_id": self.enterprise_id,
                "installed_at": datetime.now().timestamp(),
            }
        )
        self.mock_create_issue_context = patch("listeners.functions.create_issue.CONTEXT", self.mock_context)
        self.mock_jira_client_context = patch("jira.client.CONTEXT", self.mock_context)
        self.mock_jira_client_context.start()
        self.mock_create_issue_context.start()

    def teardown_method(self):
        self.mock_create_issue_context.stop()
        self.mock_jira_client_context.stop()
        restore_os_env(self.old_os_env)

    def test_create_issue(self):
        mock_ack = MagicMock()
        mock_fail = MagicMock()
        mock_complete = MagicMock()
        mock_context = MagicMock(team_id=self.team_id, enterprise_id=self.enterprise_id)
        mock_client = Mock(spec=WebClient)
        mock_inputs = {
            "user_context": {"id": self.user_id},
            "project": "PROJ",
            "issuetype": "Bug",
            "summary": "this is a test from python",
            "description": "this is a test from python",
        }

        with patch.object(requests, "request") as mock_requests:
            mock_requests.return_value = mock_response(
                status=201,
                data={
                    "id": "1234",
                    "key": "PROJ-1",
                    "self": "https://jira-dev/rest/api/2/issue/1234",
                },
            )
            create_issue_callback(
                ack=mock_ack,
                inputs=mock_inputs,
                fail=mock_fail,
                complete=mock_complete,
                context=mock_context,
                client=mock_client,
                logger=logging.getLogger(),
            )

        mock_fail.assert_not_called()
        mock_requests.assert_called_once()
        mock_ack.assert_called_once()
        mock_complete.assert_called_once()
        assert mock_complete.call_args[1] == {"outputs": {"issue_url": "https://jira-dev/browse/PROJ-1"}}

    def test_create_issue_fail(self):
        mock_ack = MagicMock()
        mock_fail = MagicMock()
        mock_complete = MagicMock()
        mock_context = MagicMock(team_id=self.team_id, enterprise_id=self.enterprise_id)
        mock_client = Mock(spec=WebClient)
        mock_inputs = {
            "user_context": {"id": "wrong_id"},
            "project": "PROJ",
            "issuetype": "Bug",
            "summary": "this is a test from python",
            "description": "this is a test from python",
        }

        with patch.object(requests, "request") as mock_requests:
            mock_requests.return_value = mock_response(
                status=201,
                data={
                    "id": "1234",
                    "key": "PROJ-1",
                    "self": "https://jira-dev/rest/api/2/issue/1234",
                },
            )
            create_issue_callback(
                ack=mock_ack,
                inputs=mock_inputs,
                fail=mock_fail,
                complete=mock_complete,
                context=mock_context,
                client=mock_client,
                logger=logging.getLogger(),
            )

        mock_ack.assert_called_once()
        mock_fail.assert_called_once()
        mock_requests.assert_not_called()
        mock_complete.assert_not_called()
