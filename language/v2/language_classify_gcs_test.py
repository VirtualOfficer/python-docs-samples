#
# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

import language_classify_gcs


def test_sample_classify_text_gcs(capsys: ...) -> None:
    assert os.environ["GOOGLE_CLOUD_PROJECT"] != ""

    language_classify_gcs.sample_classify_text()
    captured = capsys.readouterr()
    assert (
        "TV" in captured.out
        or "Movies" in captured.out
        or "Entertainment" in captured.out
    )
