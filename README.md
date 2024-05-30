# Bolt for Python Jira Functions

This is a Bolt for Python app used to interact with Jira Server.

Before getting started, make sure you have a development workspace where you
have permissions to install apps. If you don’t have one setup, go ahead and
[create one](https://slack.com/create).

## Installation

### Install the Slack CLI

To use this template, you need to install and configure the Slack CLI.
Step-by-step instructions can be found in our
[Quickstart Guide](https://api.slack.com/automation/quickstart).

### Create a Slack App

```zsh
# Clone this project onto your machine
slack create my-app -t slack-samples/bolt-python-jira-functions

# Change into the project directory
cd my-app

# Set up virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Environment Variables

Before you can run the app, you'll need to store some environment variables.

1. Rename `.env.sample` to `.env`
2. Follow these
   [Jira Instruction](https://confluence.atlassian.com/adminjiraserver0909/configure-an-incoming-link-1251415519.html)
   to get the `Client ID` (`JIRA_CLIENT_ID`) and `Client secret`
   (`JIRA_CLIENT_SECRET`) values.
3. Populate the other environment variable value with proper values.

### Running Your Project Locally

You'll know an app is the development version if the name has the string
`(local)` appended.

```zsh
# Run Bolt server
slack run

INFO:slack_bolt.App:Starting to receive messages from a new connection
```

To stop running locally, press `<CTRL> + C` to end the process.

#### Linting

```zsh
# Run ruff from root directory for linting
ruff check

# Run ruff from root directory for code formatting
ruff format
ruff check --fix
```

## Testing

For an example of how to test a function, see
`tests/functions/test_create_issue.py`.

Run all tests with:

```zsh
pytest tests/
```

## Project Structure

### `.slack/`

Contains `apps.dev.json` and `apps.json`, which include installation details for
development and deployed apps.

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

### `/jira`

Every request that needs to authenticate or interact with Jira can use the modules inside this directory.
We've grouped these resources by what actions they do
group each listener based on the Slack Platform feature used, so
`/listeners/shortcuts` handles incoming
[Shortcuts](https://api.slack.com/interactivity/shortcuts) requests,
`/listeners/views` handles
[View submissions](https://api.slack.com/reference/interaction-payloads/views#view_submission)
and so on.

### `slack.json`

Used by the CLI to interact with the project's SDK dependencies. It contains
script hooks that are executed by the CLI and implemented by the SDK.
