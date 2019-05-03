#!/usr/bin/env python

# Copyright 2019 Google LLC
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

"""Tests for automl_vision_edge_container_predict.

The test will automatically start a container with a sample saved_model.pb, send
a request with one image, verify the response and delete the started container.

If you want to try the test, please install
[gsutil tools](https://cloud.google.com/storage/docs/gsutil_install) and
[Docker CE](https://docs.docker.com/install/) first.

Examples:
sudo python -m pytest automl_vision_edge_container_predict_test.py
"""

import os
import subprocess
import time
import automl_vision_edge_container_predict as predict
import pytest


# The absolute path of the current file. This will locate the model_path when
# run docker containers.
ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
MODEL_PATH = os.path.join(ROOT_DIR, 'model_path')
# The cpu docker gcs path is from 'Edge container tutorial'.
CPU_DOCKER_GCS_PATH = 'gcr.io/automl-vision-ondevice/gcloud-container-1.12.0:latest'
# The path of a sample saved model.
SAMPLE_SAVED_MODEL = 'gs://cloud-samples-data/vision/edge_container_predict/saved_model.pb'


@pytest.fixture
def edge_container_predict():
  # set up
  # Pull the CPU docker.
  subprocess.check_output(['docker', 'pull', CPU_DOCKER_GCS_PATH])
  # Get the sample saved model.

  if not os.path.exists(MODEL_PATH):
    os.mkdir(MODEL_PATH)
  subprocess.check_output(
      ['gsutil', '-m', 'cp', SAMPLE_SAVED_MODEL, MODEL_PATH])

  yield None

  # tear down
  # Remove the docker image.
  subprocess.check_output(['docker', 'rmi', CPU_DOCKER_GCS_PATH])


def test_edge_container_predict(capsys, edge_container_predict):
  # Start the CPU docker.
  name = 'AutomlVisionEdgeContainerPredictTest'
  port_number = 8505
  subprocess.Popen(['docker', 'run', '--rm', '--name', name, '-v',
                    MODEL_PATH + ':/tmp/mounted_model/0001', '-p',
                    str(port_number) + ':8501', '-t',
                    CPU_DOCKER_GCS_PATH])
  # Sleep a few seconds to wait for the container running.
  time.sleep(10)

  image_file_path = 'test.jpg'
  # If you send requests with one image each time, the key value does not
  # matter. If you send requests with multiple images, please used different
  # keys to indicated different images.
  image_key = '1'
  # Send a request.
  response = predict.container_predict(
      image_file_path, image_key, port_number)

  # Stop the container.
  subprocess.check_output(['docker', 'stop', name])

  # Verify the response.
  assert 'predictions' in response
  assert 'key' in response['predictions'][0]
  assert image_key == response['predictions'][0]['key']
