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

"""Google Cloud Speech API sample application using the REST API for batch
processing.

Example usage:
    python transcribe.py resources/audio.raw
    python transcribe.py gs://cloud-samples-tests/speech/brooklyn.flac
"""

# [START import_libraries]
import argparse
import io
# [END import_libraries]


def transcribe_file(speech_file):
    """Transcribe the given audio file."""
    from google.cloud.gapic.speech.v1 import speech_client
    from google.cloud.gapic.speech.v1 import enums
    from google.cloud.proto.speech.v1 import cloud_speech_pb2
    client = speech_client.SpeechClient()

    with io.open(speech_file, 'rb') as audio_file:
        content = audio_file.read()
        audio = cloud_speech_pb2.RecognitionAudio(content=content)

        encoding = enums.RecognitionConfig.AudioEncoding.LINEAR16
        sample_rate_hertz = 16000
        language_code = 'en-US'
        config = cloud_speech_pb2.RecognitionConfig(
            encoding=encoding,
            sample_rate_hertz=sample_rate_hertz,
            language_code=language_code)

    response = client.recognize(config, audio)
    alternatives = response.results[0].alternatives

    for alternative in alternatives:
        print('Transcript: {}'.format(alternative.transcript))


def transcribe_gcs(gcs_uri):
    """Transcribes the audio file specified by the gcs_uri."""
    from google.cloud.gapic.speech.v1 import speech_client
    from google.cloud.gapic.speech.v1 import enums
    from google.cloud.proto.speech.v1 import cloud_speech_pb2
    client = speech_client.SpeechClient()
    audio = cloud_speech_pb2.RecognitionAudio(uri=gcs_uri)

    encoding = enums.RecognitionConfig.AudioEncoding.FLAC
    sample_rate_hertz = 16000
    language_code = 'en-US'
    config = cloud_speech_pb2.RecognitionConfig(
        encoding=encoding,
        sample_rate_hertz=sample_rate_hertz,
        language_code=language_code)

    response = client.recognize(config, audio)
    alternatives = response.results[0].alternatives

    for alternative in alternatives:
        print('Transcript: {}'.format(alternative.transcript))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        'path', help='File or GCS path for audio file to be recognized')
    args = parser.parse_args()
    if args.path.startswith('gs://'):
        transcribe_gcs(args.path)
    else:
        transcribe_file(args.path)
