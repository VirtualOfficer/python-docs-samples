#!/usr/bin/env python

# Copyright 2017 Google Inc. All Rights Reserved.
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

"""This application demonstrates face detection, label detection,
explicit content, and shot change detection using the Google Cloud API.

Usage Examples:
    python beta_snippets.py boxes \
    gs://python-docs-samples-tests/video/googlework_short.mp4

    python beta_snippets.py \
    emotions gs://python-docs-samples-tests/video/googlework_short.mp4
"""

import argparse

from google.cloud import videointelligence_v1beta2 as videointelligence


# [START video_face_bounding_boxes]
def face_bounding_boxes(path):
    """ Detects faces' bounding boxes. """
    video_client = videointelligence.VideoIntelligenceServiceClient()
    features = [videointelligence.enums.Feature.FACE_DETECTION]

    config = videointelligence.types.FaceConfig(
        include_bounding_boxes=True)
    context = videointelligence.types.VideoContext(
        face_detection_config=config)

    operation = video_client.annotate_video(
        path, features=features, video_context=context)
    print('\nProcessing video for face annotations:')

    result = operation.result(timeout=900)
    print('\nFinished processing.')

    # There is only one result because a single video was processed.
    faces = result.annotation_results[0].face_detection_annotations
    for i, face in enumerate(faces):
        print('Face {}'.format(i))

        # Each face_detection_annotation has only one segment.
        segment = face.segments[0]
        start_time = (segment.segment.start_time_offset.seconds +
                      segment.segment.start_time_offset.nanos / 1e9)
        end_time = (segment.segment.end_time_offset.seconds +
                    segment.segment.end_time_offset.nanos / 1e9)
        positions = '{}s to {}s'.format(start_time, end_time)
        print('\tSegment: {}\n'.format(positions))

        # There are typically many frames for each face,
        # here we print information on only the first frame.
        frame = face.frames[0]

        time_offset = (frame.time_offset.seconds +
                       frame.time_offset.nanos / 1e9)
        box = frame.attributes[0].normalized_bounding_box

        print('First frame time offset: {}s\n'.format(time_offset))

        print('First frame normalized bounding box:')
        print('\tleft  : {}'.format(box.left))
        print('\ttop   : {}'.format(box.top))
        print('\tright : {}'.format(box.right))
        print('\tbottom: {}'.format(box.bottom))
        print('\n')
# [END video_face_bounding_boxes]


# [START video_face_emotions]
def face_emotions(path):
    """ Analyze faces' emotions over frames. """
    video_client = videointelligence.VideoIntelligenceServiceClient()
    features = [videointelligence.enums.Feature.FACE_DETECTION]

    # include_bounding_boxes must be set to True for include_emotions
    # to work.
    config = videointelligence.types.FaceConfig(
        include_bounding_boxes=True,
        include_emotions=True)
    context = videointelligence.types.VideoContext(
        face_detection_config=config)

    operation = video_client.annotate_video(
        path, features=features, video_context=context)
    print('\nProcessing video for face annotations:')

    result = operation.result(timeout=600)
    print('\nFinished processing.')

    # There is only one result because a single video was processed.
    faces = result.annotation_results[0].face_detection_annotations
    for i, face in enumerate(faces):
        print('Face {}'.format(i))

        frame_emotions = []
        for frame in face.frames:
            time_offset = (frame.time_offset.seconds +
                           frame.time_offset.nanos / 1e9)
            emotions = frame.attributes[0].emotions

            # from videointelligence.enums
            emotion_labels = (
                'EMOTION_UNSPECIFIED', 'AMUSEMENT', 'ANGER',
                'CONCENTRATION', 'CONTENTMENT', 'DESIRE',
                'DISAPPOINTMENT', 'DISGUST', 'ELATION',
                'EMBARRASSMENT', 'INTEREST', 'PRIDE', 'SADNESS',
                'SURPRISE')

            emotion, score = sorted(
                [(em.emotion, em.score) for em in emotions],
                key=lambda p: p[1])[-1]
            emotion_label = emotion_labels[emotion]

            frame_emotions.append((time_offset, emotion_label, score))

        frame_emotions = sorted(frame_emotions, key=lambda p: p[0])
        for time_offset, emotion_label, score in frame_emotions:
            print('\t{:04.2f}s: {:14}({:4.3f})'.format(
                time_offset, emotion_label, score))
        print('\n')
# [END video_face_emotions]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    subparsers = parser.add_subparsers(dest='command')
    analyze_faces_parser = subparsers.add_parser(
        'boxes', help=face_bounding_boxes.__doc__)
    analyze_faces_parser.add_argument('path')

    analyze_emotions_parser = subparsers.add_parser(
        'emotions', help=face_emotions.__doc__)
    analyze_emotions_parser.add_argument('path')

    args = parser.parse_args()

    if args.command == 'boxes':
        face_bounding_boxes(args.path)
    elif args.command == 'emotions':
        face_emotions(args.path)
