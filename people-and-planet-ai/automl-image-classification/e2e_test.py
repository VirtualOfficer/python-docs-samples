# Copyright 2021 Google LLC
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

from datetime import datetime
import os
import subprocess
import uuid

from google.cloud import bigquery
from google.cloud import storage
import pytest

SUFFIX = uuid.uuid4().hex[0:6]
PROJECT = os.environ["GOOGLE_CLOUD_PROJECT"]
BUCKET_NAME = f"wildlife-insights-test-{SUFFIX}"
BIGQUERY_DATASET = f"wildlife_insights_test_{SUFFIX}"
BIGQUERY_TABLE = "images_database"
REGION = "us-central1"
MIN_IMAGES_PER_CLASS = 1
MAX_IMAGES_PER_CLASS = 1
JOB_SUFFIX = f"{datetime.now().strftime('%Y%m%d-%H%M')}-{SUFFIX}"


@pytest.fixture(scope="session")
def bucket_name() -> str:
    storage_client = storage.Client()
    bucket = storage_client.create_bucket(BUCKET_NAME)

    yield BUCKET_NAME

    # This test creates 1 image file per class, creating around 650 files.
    # `bucket.delete(force=True)` does not work if the bucket has >256 files.
    # Sequentially deleting many files with the client libraries can take
    # several minutes, so we're using `gsutil -m` instead.
    subprocess.call(["gsutil", "-m", "rm", "-rf", f"gs:://{BUCKET_NAME}/*"])
    bucket.delete(force=True)


@pytest.fixture(scope="session")
def bigquery_dataset() -> str:
    bigquery_client = bigquery.Client()

    dataset_id = f"{PROJECT}.{BIGQUERY_DATASET}"
    bigquery_client.create_dataset(bigquery.Dataset(dataset_id))

    yield BIGQUERY_DATASET

    bigquery_client.delete_dataset(dataset_id, delete_contents=True, not_found_ok=True)


@pytest.fixture(scope="session")
def bigquery_table(bucket_name: str, bigquery_dataset: str) -> None:
    # Create the images database table.
    subprocess.run(
        [
            "python",
            "pipeline.py",
            "--create-images-database",
            f"--project={PROJECT}",
            f"--job_name=wildlife-images-database-{JOB_SUFFIX}",
            f"--cloud-storage-path=gs://{bucket_name}",
            f"--bigquery-dataset={bigquery_dataset}",
            f"--bigquery-table={BIGQUERY_TABLE}",
            "--runner=DataflowRunner",
            f"--region={REGION}",
            "--worker_machine_type=n1-standard-2",
        ],
        check=True,
    )

    # The table is deleted when we delete the dataset.
    yield BIGQUERY_TABLE


def test_end_to_end(
    bucket_name: str, bigquery_dataset: str, bigquery_table: str
) -> None:
    subprocess.run(
        [
            "python",
            "pipeline.py",
            f"--project={PROJECT}",
            f"--job_name=wildlife-train-{JOB_SUFFIX}",
            f"--cloud-storage-path=gs://{bucket_name}",
            f"--bigquery-dataset={bigquery_dataset}",
            f"--bigquery-table={bigquery_table}",
            "--automl-name-prefix=",  # empty skips the AutoML operations.
            f"--min-images-per-class={MIN_IMAGES_PER_CLASS}",
            f"--max-images-per-class={MAX_IMAGES_PER_CLASS}",
            "--runner=DataflowRunner",
            "--requirements_file=requirements.txt",
            f"--region={REGION}",
        ],
        check=True,
    )
