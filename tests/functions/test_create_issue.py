import json
import logging
import os
from unittest.mock import MagicMock, patch

import requests
from controllers import PersonalAccessTokenTable

from listeners.functions.create_issue import create_issue_callback
from tests.utils import remove_os_env_temporarily, restore_os_env


def mock_response(status=200, data: dict = None):
    mock_resp = MagicMock()
    mock_resp.status_code = status
    if data:
        mock_resp.json = MagicMock(return_value=data)
        mock_resp.text = json.dumps(data)
    return mock_resp


class TestCreateIssue:
    def setup_method(self):
        self.old_os_env = remove_os_env_temporarily()
        PersonalAccessTokenTable().clear()

    def teardown_method(self):
        PersonalAccessTokenTable().clear()
        restore_os_env(self.old_os_env)

    def test_create_issue(self):
        mock_ack = MagicMock()
        mock_fail = MagicMock()
        mock_complete = MagicMock()
        mock_input = {
            "user_id": "me",
            "project": "PROJ",
            "issuetype": "Bug",
            "summary": "this is a test from python",
            "description": "this is a test from python",
        }
        PersonalAccessTokenTable().create_user("me", "my_pat_token")

        os.environ["JIRA_BASE_URL"] = "https://jira-dev/"

        with patch.object(requests, "post") as mock_requests:
            mock_requests.return_value = mock_response(
                status=201,
                data={
                    "id": "1234",
                    "key": "PROJ-1",
                    "self": "https://jira-dev/rest/api/2/issue/1234",
                },
            )
            create_issue_callback(mock_ack, mock_input, mock_fail, mock_complete, logging.getLogger())
            mock_requests.assert_called_once()

        mock_ack.assert_called_once()
        mock_complete.assert_called_once()
        assert mock_complete.call_args[1] == {"outputs": {"issue_url": "https://jira-dev/rest/api/2/issue/1234"}}
