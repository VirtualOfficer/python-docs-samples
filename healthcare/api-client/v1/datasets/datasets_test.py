# Copyright 2020 Google LLC All Rights Reserved.
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

import os
import pytest
import uuid

import datasets

cloud_region = 'us-central1'
project_id = os.environ['GOOGLE_CLOUD_PROJECT']

dataset_id = 'test-dataset-{}'.format(uuid.uuid4())
destination_dataset_id = 'test-destination-dataset-{}'.format(uuid.uuid4())
keeplist_tags = 'PatientID'
time_zone = 'UTC'


@pytest.fixture(scope="module")
def test_dataset():
    dataset = datasets.create_dataset(
        project_id, cloud_region, dataset_id
    )

    yield dataset

    # Clean up
    datasets.delete_dataset(project_id, cloud_region, dataset_id)


def test_CRUD_dataset(capsys):
    datasets.create_dataset(
        project_id,
        cloud_region,
        dataset_id)

    datasets.get_dataset(
        project_id, cloud_region, dataset_id)

    datasets.list_datasets(
        project_id, cloud_region)

    datasets.delete_dataset(
        project_id, cloud_region, dataset_id)

    out, _ = capsys.readouterr()

    # Check that create/get/list/delete worked
    assert 'Created dataset' in out
    assert 'Time zone' in out
    assert 'Dataset' in out
    assert 'Deleted dataset' in out


def test_patch_dataset(capsys, test_dataset):
    datasets.patch_dataset(
        project_id,
        cloud_region,
        dataset_id,
        time_zone)

    out, _ = capsys.readouterr()

    # Check that the patch to the time zone worked
    assert 'UTC' in out


def test_deidentify_dataset(capsys, test_dataset):
    datasets.deidentify_dataset(
        project_id,
        cloud_region,
        dataset_id,
        destination_dataset_id,
        keeplist_tags)

    # Delete the destination_dataset_id which
    # is created as part of the de-id test.
    datasets.delete_dataset(
        project_id,
        cloud_region,
        destination_dataset_id)

    out, _ = capsys.readouterr()

    # Check that de-identify worked
    assert 'De-identified data written to' in out


def test_get_set_dataset_iam_policy(capsys, test_dataset):
    get_response = datasets.get_dataset_iam_policy(
        project_id,
        cloud_region,
        dataset_id)

    set_response = datasets.set_dataset_iam_policy(
        project_id,
        cloud_region,
        dataset_id,
        'serviceAccount:python-docs-samples-tests@appspot.gserviceaccount.com',
        'roles/viewer')

    out, _ = capsys.readouterr()

    assert 'etag' in get_response
    assert 'bindings' in set_response
    assert len(set_response['bindings']) == 1
    assert 'python-docs-samples-tests' in str(set_response['bindings'])
    assert 'roles/viewer' in str(set_response['bindings'])
