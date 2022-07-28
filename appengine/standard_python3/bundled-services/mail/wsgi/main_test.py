# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import subprocess
import time
import uuid

import pytest
import requests


def gcloud_cli(command, retries=3):
    """
    Runs the gcloud CLI with given options, parses the json formatted output
    and returns the resulting Python object.

    Automatically retries with delays unless retries=0 is specified.

    Usage: gcloud_cli(options, retries=retries)
        options: command line options
        retries: how many times to retry is gcloud CLI fails with error

    Example:
        result = gcloud_cli("app deploy --no-promote")
        print(f"Deployed version {result['versions'][0]['id']}")

    Raises Exception with the stderr output of the last attempt if all
    retries fail.
    """
    for retry in range(retries):
        time.sleep(retry * 5)  # Wait 0, 5, 10, 15, etc seconds before next try

        output = subprocess.run(
            f"gcloud {command} --quiet --format=json",
            capture_output=True,
            shell=True,
        )
        try:
            entries = json.loads(output.stdout)
            return entries
        except Exception:
            print(f"gcloud_cli attempt {retry}: Failed to read log")
            print(f"gcloud_cli attempt {retry}: gcloud stderr was {output.stderr}")

    raise Exception(f"gcloud_cli attempt {retry}: gcloud stderr was {output.stderr}")


@pytest.fixture
def version():
    """Launch a new version of the app for testing, and yield the
    project and version number so tests can invoke it, then delete it.
    """

    result = gcloud_cli(f"app deploy --no-promote --version={uuid.uuid4().hex}")
    version_id = result["versions"][0]["id"]
    project_id = result["versions"][0]["project"]

    yield project_id, version_id

    gcloud_cli(f"app versions delete {version_id}", retries=1)


def test_send_receive(version):
    project_id, version_id = version
    version_hostname = f"{version_id}-dot-{project_id}.appspot.com"

    # Check that version is serving form in home page
    response = requests.get(f"https://{version_hostname}/")
    assert response.status_code == 200
    assert '<form action="" method="POST">' in response.text

    # Send valid mail
    response = requests.post(
        f"https://{version_hostname}/",
        data={
            "email": f"valid-user@{version_id}-dot-{project_id}.appspotmail.com",
            "body": "This message should be delivered",
        },
    )

    assert response.status_code == 201
    assert "Successfully sent mail" in response.text

    # Give the mail some time to be delivered and logs to post
    time.sleep(30)

    # Fetch logs to check messages on received mail
    entries = gcloud_cli(
        f'logging read "resource.type=gae_app AND resource.labels.version_id={version_id}"'
    )

    text_payloads = ""
    for entry in entries:
        if "textPayload" in entry:
            text_payloads += entry["textPayload"]
            text_payloads += "\n"

    expected = f"Received greeting for valid-user@{version_id}-dot-{project_id}.appspotmail.com"
    assert expected in text_payloads
    assert "This message should be delivered" in text_payloads
