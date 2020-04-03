# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import os

import job_search_get_tenant

PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]
TENANT_ID = os.environ["JOB_SEARCH_TENANT_ID"]


def test_get_tenant(capsys):
    job_search_get_tenant.get_tenant(PROJECT_ID, TENANT_ID)
    out, _ = capsys.readouterr()
    assert "Name: " in out
