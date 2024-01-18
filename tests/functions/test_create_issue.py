import logging
import os
from unittest.mock import MagicMock

from controllers import PersonalAccessTokenTable
from listeners.functions.create_issue import create_issue_callback


from tests.utils import remove_os_env_temporarily, restore_os_env


class TestCreateIssue:
    def setup_method(self):
        self.old_os_env = remove_os_env_temporarily()

    def teardown_method(self):
        restore_os_env(self.old_os_env)

    def test_create_issue(self, caplog):
        mock_ack = MagicMock(retrun_value=None)
        mock_fail = MagicMock()
        mock_complete = MagicMock()
        mock_logger = logging.getLogger()
        mock_input = {
            "user_id": "me",
            "project": "HERMES",
            "issuetype": "BUG",
            "summary": "this is a test from python",
            "description": "this is a test from python",
        }

        os.environ["JIRA_BASE_URL"] = "https://jira-dev.tinyspeck.com/"
        mock_pat_table = PersonalAccessTokenTable()
        mock_pat_table.create_user("me", "1234")
        create_issue_callback(mock_ack, mock_input, mock_fail, mock_complete, mock_logger, mock_pat_table)

        mock_complete.assert_called_once()
