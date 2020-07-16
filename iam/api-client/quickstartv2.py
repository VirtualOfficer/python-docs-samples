#!/usr/bin/env python
#
# Copyright 2020 Google Inc. All Rights Reserved.
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

# [START iam_quickstartv2]
import os

from google.oauth2 import service_account
import googleapiclient.discovery


def quickstart(project_id, member):
    """Gets a policy, adds a member, prints their permissions, and removes the member."""

    # Role to be granted.
    role = "roles/logging.logWriter"

    # Initializes service.
    crm_service = initialize_service()

    # Grants your member the 'Log Writer' role for the project.
    modify_policy_add_role(crm_service, project_id, role, member)

    # Gets the project's policy and prints all members with the 'Log Writer' role.
    policy = get_policy(crm_service, project_id)
    binding = next(b for b in policy["bindings"] if b["role"] == role)
    print(f'Role: {(binding["role"])}')
    print("Members: ")
    for m in binding["members"]:
        print(f'[{m}]')

    # Removes the member from the 'Log Writer' role.
    modify_policy_remove_member(crm_service, project_id, role, member)


def initialize_service():
    """Initializes a Cloud Resource Manager service."""

    credentials = service_account.Credentials.from_service_account_file(
        filename=os.environ["GOOGLE_APPLICATION_CREDENTIALS"],
        scopes=["https://www.googleapis.com/auth/cloud-platform"],
    )
    crm_service = googleapiclient.discovery.build(
        "cloudresourcemanager", "v1", credentials=credentials
    )
    return crm_service


def modify_policy_add_role(crm_service, project_id, role, member):
    """Adds a new role binding to a policy."""

    policy = get_policy(crm_service, project_id)

    if role in policy["bindings"]:
        binding = next(b for b in policy["bindings"] if b["role"] == role)
        binding["members"].append(member)
    else:
        binding = {"role": role, "members": [member]}
        policy["bindings"].append(binding)

    set_policy(crm_service, project_id, policy)


def modify_policy_remove_member(crm_service, project_id, role, member):
    """Removes a  member from a role binding."""

    policy = get_policy(crm_service, project_id)

    binding = next(b for b in policy["bindings"] if b["role"] == role)
    if "members" in binding and member in binding["members"]:
        binding["members"].remove(member)

    set_policy(crm_service, project_id, policy)


def get_policy(crm_service, project_id, version=3):
    """Gets IAM policy for a project."""

    policy = (
        crm_service.projects()
        .getIamPolicy(
            resource=project_id,
            body={"options": {"requestedPolicyVersion": version}},
        )
        .execute()
    )
    return policy


def set_policy(crm_service, project_id, policy):
    """Sets IAM policy for a project."""

    policy = (
        crm_service.projects()
        .setIamPolicy(resource=project_id, body={"policy": policy})
        .execute()
    )
    return policy


if __name__ == '__main__':

    # TODO: replace with your project ID
    project_id = "test-project-1000092"
    # TODO: Replace with the ID of your member in the form 'user:member@example.com.
    member = "user:melaniedejong@google.com"
    quickstart(project_id, member)
# [END iam_quickstartv2]
