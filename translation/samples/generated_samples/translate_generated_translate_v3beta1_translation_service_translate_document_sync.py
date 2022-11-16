# -*- coding: utf-8 -*-
# Copyright 2020 Google LLC
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
#
# Generated code. DO NOT EDIT!
#
# Snippet for TranslateDocument
# NOTE: This snippet has been automatically generated for illustrative purposes only.
# It may require modifications to work in your environment.

# To install the latest published package dependency, execute the following:
#   python3 -m pip install google-cloud-translate


# [START translate_generated_translate_v3beta1_TranslationService_TranslateDocument_sync]
from google.cloud import translate_v3beta1


def sample_translate_document():
    # Create a client
    client = translate_v3beta1.TranslationServiceClient()

    # Initialize request argument(s)
    document_input_config = translate_v3beta1.DocumentInputConfig()
    document_input_config.content = b'content_blob'

    request = translate_v3beta1.TranslateDocumentRequest(
        parent="parent_value",
        target_language_code="target_language_code_value",
        document_input_config=document_input_config,
    )

    # Make the request
    response = client.translate_document(request=request)

    # Handle the response
    print(response)

# [END translate_generated_translate_v3beta1_TranslationService_TranslateDocument_sync]
