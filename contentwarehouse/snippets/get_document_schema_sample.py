# Copyright 2023 Google LLC
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


# [START contentwarehouse_get_document_schema]
from google.api_core.client_options import ClientOptions
from google.cloud import contentwarehouse

# TODO(developer): Uncomment these variables before running the sample.
# project_number = "YOUR_PROJECT_NUMBER"
# location = "YOUR_PROJECT_LOCATION" # Format is "us" or "eu"
# document_schema_id = "YOUR_DOCUMENT SCHEMA_ID"


def sample_get_document_schema(
    project_number: str, location: str, document_schema_id: str
) -> None:
    """Gets document schema details.

    Args:
        project_number: Google Cloud project number.
        location: Google Cloud project location.
        document_schema_id: Unique identifier for document schema
    Returns:
        Response object.
    """
    # You must set the `api_endpoint` if you use a location other than "us".
    client_options = ClientOptions(
        api_endpoint=f"{location}-contentwarehouse.googleapis.com"
    )
    # Create a Schema Service client.
    document_schema_client = contentwarehouse.DocumentSchemaServiceClient(
        client_options=client_options
    )

    # The full resource name of the location, e.g.:
    # projects/{project_number}/locations/{location}/documentSchemas/{document_schema_id}
    document_schema_path = document_schema_client.document_schema_path(
        project=project_number,
        location=location,
        document_schema=document_schema_id,
    )

    # Initialize request argument(s)
    request = contentwarehouse.GetDocumentSchemaRequest(
        name=document_schema_path,
    )

    # Make the request
    response = document_schema_client.get_document_schema(request=request)

    # Handle the response
    print("Document Schema:", response)

    return response


# [END contentwarehouse_get_document_schema]
