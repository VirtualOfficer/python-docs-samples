#!/usr/bin/env python

# Copyright 2017 Google Inc. All Rights Reserved.
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

"""Google Cloud Speech API sample application using the REST API for async
batch processing.

Example usage: python transcribe_async.py resources/audio.raw
"""

# [START import_libraries]
import argparse
import io
import time
# [END import_libraries]


def main(speech_file):
    """Transcribe the given audio file asynchronously.

    Args:
        speech_file: the name of the audio file.
    """
    # [START authenticating]
    # Application default credentials provided by env variable
    # GOOGLE_APPLICATION_CREDENTIALS
    from google.cloud import speech
    speech_client = speech.Client()
    # [END authenticating]

    # [START construct_request]
    # Loads the audio into memory
    with io.open(speech_file, 'rb') as audio_file:
        content = audio_file.read()
        audio_sample = speech_client.sample(
            content,
            source_uri=None,
            encoding='LINEAR16',
            sample_rate=16000)
    # [END construct_request]

    # [START send_request]
    operation = speech_client.speech_api.async_recognize(audio_sample)

    retry_count = 100
    while retry_count > 0 and not operation.complete:
        retry_count -= 1
        time.sleep(2)
        operation.poll()

    if not operation.complete:
        print("Operation not complete and retry limit reached.")
        return

    alternatives = operation.results
    for alternative in alternatives:
        print('Transcript: {}'.format(alternative.transcript))
        print('Confidence: {}'.format(alternative.confidence))
    # [END send_request]


# [START run_application]
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        'speech_file', help='Full path of audio file to be recognized')
    args = parser.parse_args()
    main(args.speech_file)
    # [END run_application]
