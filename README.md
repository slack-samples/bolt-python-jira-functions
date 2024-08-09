# Bolt for Python Jira Functions

This is a Bolt for Python app used to interact with Jira Server through custom functions in
[Workflow Builder](https://api.slack.com/start#workflow-builder).

## Setup

Before getting started, make sure you have a development workspace where you
have permissions to install apps. If you don’t have one setup, go ahead and
[create one](https://slack.com/create).

### Developer Program

Join the [Slack Developer Program](https://api.slack.com/developer-program) for
exclusive access to beta features, tooling, and resources created to help
developers build and grow.

## Installation

### Create a Slack App

1. Open [https://api.slack.com/apps/new](https://api.slack.com/apps/new) and
   choose "From an app manifest"
2. Choose the workspace you want to install the application to
3. Copy the contents of [manifest.json](./manifest.json) into the text box that
   says `*Paste your manifest code here*` (within the JSON tab) and click _Next_
4. Review the configuration and click _Create_
5. Click _Install to Workspace_ and _Allow_ on the screen that follows. You'll
   then be redirected to the App Configuration dashboard.

### Environment Variables

Before you can run the app, you'll need to store some environment variables.

1. Rename `.example.env` to `.env`
2. Open your apps configuration page from this list, click **OAuth &
   Permissions** in the left hand menu, then copy the Bot User OAuth Token. You
   will store this in your environment as `SLACK_BOT_TOKEN`.
3. Click ***Basic Information** from the left hand menu and follow the steps in
   the App-Level Tokens section to create an app-level token with the
   `connections:write` scope. Copy this token. You will store this in your
   environment as `SLACK_APP_TOKEN`.
4. Follow these
   [Jira Instruction](https://confluence.atlassian.com/adminjiraserver0909/configure-an-incoming-link-1251415519.html)
   to create an external application and get the `Client ID` (`JIRA_CLIENT_ID`)
   and `Client secret` (`JIRA_CLIENT_SECRET`) values.
5. Populate the other environment variable value with proper values.

### Local Project

```zsh
# Clone this project onto your machine
git clone https://github.com/slack-samples/bolt-python-jira-functions.git

# Change into this project directory
cd bolt-python-jira-functions

# Setup your python virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install the dependencies
pip3 install -r requirements.txt

# Start your local server
python3 app.py
```

#### Linting

```zsh
# Run ruff from root directory for linting
ruff check

# Run ruff from root directory for code formatting
ruff format
ruff check --fix
```

#### Testing

For an example of how to test a function, see
`tests/functions/test_create_issue.py`.

Run all tests with:

```zsh
pytest tests/
```

## Project Structure

### `manifest.json`

`manifest.json` is a configuration for Slack apps. With a manifest, you can
create an app with a pre-defined configuration, or adjust the configuration of
an existing app.

### `app.py`

`app.py` is the entry point for the application and is the file you'll run to
start the server. This project aims to keep this file as thin as possible,
primarily using it as a way to route inbound requests.

### `/listeners`

Every incoming request is routed to a "listener". Inside this directory, we
group each listener based on the Slack Platform feature used, so
`/listeners/shortcuts` handles incoming
[Shortcuts](https://api.slack.com/interactivity/shortcuts) requests,
`/listeners/views` handles
[View submissions](https://api.slack.com/reference/interaction-payloads/views#view_submission)
and so on.
