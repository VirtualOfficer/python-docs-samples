#!/usr/bin/env python

# Copyright 2017 Google, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This application demonstrates how to perform basic operations with the
Google Cloud Natural Language API

For more information, the documentation at
https://cloud.google.com/natural-language/docs.
"""

import argparse
import sys

from google.cloud import language_v1beta2
from google.cloud.language_v1beta2 import enums
from google.cloud.language_v1beta2 import types
import six


def sentiment_text(text):
    """Detects sentiment in the text."""
    client = language_v1beta2.LanguageServiceClient()

    if isinstance(text, six.binary_type):
        text = text.decode('utf-8')

    # Instantiates a plain text document.
    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)

    # Detects sentiment in the document. You can also analyze HTML with:
    #   document.type == enums.Document.Type.HTML
    sentiment = client.analyze_sentiment(document).document_sentiment

    print('Score: {}'.format(sentiment.score))
    print('Magnitude: {}'.format(sentiment.magnitude))


def sentiment_file(gcs_uri):
    """Detects sentiment in the file located in Google Cloud Storage."""
    client = language_v1beta2.LanguageServiceClient()

    # Instantiates a plain text document.
    document = types.Document(
        gcs_content_uri=gcs_uri,
        type=enums.Document.Type.PLAIN_TEXT)

    # Detects sentiment in the document. You can also analyze HTML with:
    #   document.type == enums.Document.Type.HTML
    sentiment = client.analyze_sentiment(document).document_sentiment

    print('Score: {}'.format(sentiment.score))
    print('Magnitude: {}'.format(sentiment.magnitude))


def entities_text(text):
    """Detects entities in the text."""
    client = language_v1beta2.LanguageServiceClient()

    if isinstance(text, six.binary_type):
        text = text.decode('utf-8')

    # Instantiates a plain text document.
    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)

    # Detects entities in the document. You can also analyze HTML with:
    #   document.type == enums.Document.Type.HTML
    entities = client.analyze_entities(document).entities

    for entity in entities:
        print('=' * 20)
        print(u'{:<16}: {}'.format('name', entity.name))
        print(u'{:<16}: {}'.format('type', entity.type))
        print(u'{:<16}: {}'.format('metadata', entity.metadata))
        print(u'{:<16}: {}'.format('salience', entity.salience))
        print(u'{:<16}: {}'.format('wikipedia_url',
              entity.metadata.get('wikipedia_url', '-')))


def entities_file(gcs_uri):
    """Detects entities in the file located in Google Cloud Storage."""
    client = language_v1beta2.LanguageServiceClient()

    # Instantiates a plain text document.
    document = types.Document(
        gcs_content_uri=gcs_uri,
        type=enums.Document.Type.PLAIN_TEXT)

    # Detects sentiment in the document. You can also analyze HTML with:
    #   document.type == enums.Document.Type.HTML
    entities = client.analyze_entities(document).entities

    for entity in entities:
        print('=' * 20)
        print(u'{:<16}: {}'.format('name', entity.name))
        print(u'{:<16}: {}'.format('type', entity.type))
        print(u'{:<16}: {}'.format('metadata', entity.metadata))
        print(u'{:<16}: {}'.format('salience', entity.salience))
        print(u'{:<16}: {}'.format('wikipedia_url',
              entity.metadata.get('wikipedia_url', '-')))


def syntax_text(text):
    """Detects syntax in the text."""
    client = language_v1beta2.LanguageServiceClient()

    if isinstance(text, six.binary_type):
        text = text.decode('utf-8')

    # Instantiates a plain text document.
    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)

    # Detects syntax in the document. You can also analyze HTML with:
    #   document.type == enums.Document.Type.HTML
    tokens = client.analyze_syntax(document).tokens

    # part-of-speech tags from google.cloud.language.enums.PartOfSpeech.Tag
    pos_tag = ('UNKNOWN', 'ADJ', 'ADP', 'ADV', 'CONJ', 'DET', 'NOUN', 'NUM',
               'PRON', 'PRT', 'PUNCT', 'VERB', 'X', 'AFFIX')

    for token in tokens:
        print(u'{}: {}'.format(pos_tag[token.part_of_speech.tag],
                               token.text.content))


def syntax_file(gcs_uri):
    """Detects syntax in the file located in Google Cloud Storage."""
    client = language_v1beta2.LanguageServiceClient()

    # Instantiates a plain text document.
    document = types.Document(
        gcs_content_uri=gcs_uri,
        type=enums.Document.Type.PLAIN_TEXT)

    # Detects syntax in the document. You can also analyze HTML with:
    #   document.type == enums.Document.Type.HTML
    tokens = client.analyze_syntax(document).tokens

    # part-of-speech tags from google.cloud.language.enums.PartOfSpeech.Tag
    pos_tag = ('UNKNOWN', 'ADJ', 'ADP', 'ADV', 'CONJ', 'DET', 'NOUN', 'NUM',
               'PRON', 'PRT', 'PUNCT', 'VERB', 'X', 'AFFIX')

    for token in tokens:
        print(u'{}: {}'.format(pos_tag[token.part_of_speech.tag],
                               token.text.content))


# [START def_entity_sentiment_text]
def entity_sentiment_text(text):
    """Detects entity sentiment in the provided text."""
    client = language_v1beta2.LanguageServiceClient()

    if isinstance(text, six.binary_type):
        text = text.decode('utf-8')

    document = types.Document(
        content=text.encode('utf-8'),
        type=enums.Document.Type.PLAIN_TEXT)

    encoding = 'UTF32'
    if sys.maxunicode == 65535:
        encoding = 'UTF16'

    result = client.analyze_entity_sentiment(
        document, encoding)

    for entity in result.entities:
        print('Mentions: ')
        print(u'Name: "{}"'.format(entity.name))
        for mention in entity.mentions:
            print(u'  Begin Offset : {}'.format(mention.text.begin_offset))
            print(u'  Content : {}'.format(mention.text.content))
            print(u'  Magnitude : {}'.format(mention.sentiment.magnitude))
            print(u'  Sentiment : {}'.format(mention.sentiment.score))
            print(u'  Type : {}'.format(mention.type))
        print(u'Salience: {}'.format(entity.salience))
        print(u'Sentiment: {}\n'.format(entity.sentiment))
# [END def_entity_sentiment_text]


def entity_sentiment_file(gcs_uri):
    """Detects entity sentiment in a Google Cloud Storage file."""
    client = language_v1beta2.LanguageServiceClient()

    document = types.Document(
        gcs_content_uri=gcs_uri,
        type=enums.Document.Type.PLAIN_TEXT)

    encoding = 'UTF32'
    if sys.maxunicode == 65535:
        encoding = 'UTF16'

    result = client.analyze_entity_sentiment(
      document, encoding)

    for entity in result.entities:
        print(u'Name: "{}"'.format(entity.name))
        for mention in entity.mentions:
            print(u'  Begin Offset : {}'.format(mention.text.begin_offset))
            print(u'  Content : {}'.format(mention.text.content))
            print(u'  Magnitude : {}'.format(mention.sentiment.magnitude))
            print(u'  Sentiment : {}'.format(mention.sentiment.score))
            print(u'  Type : {}'.format(mention.type))
        print(u'Salience: {}'.format(entity.salience))
        print(u'Sentiment: {}\n'.format(entity.sentiment))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    subparsers = parser.add_subparsers(dest='command')

    sentiment_entities_text_parser = subparsers.add_parser(
        'sentiment-entities-text', help=entity_sentiment_text.__doc__)
    sentiment_entities_text_parser.add_argument('text')

    sentiment_entities_file_parser = subparsers.add_parser(
        'sentiment-entities-file', help=entity_sentiment_file.__doc__)
    sentiment_entities_file_parser.add_argument('gcs_uri')

    sentiment_text_parser = subparsers.add_parser(
        'sentiment-text', help=sentiment_text.__doc__)
    sentiment_text_parser.add_argument('text')

    sentiment_file_parser = subparsers.add_parser(
        'sentiment-file', help=sentiment_file.__doc__)
    sentiment_file_parser.add_argument('gcs_uri')

    entities_text_parser = subparsers.add_parser(
        'entities-text', help=entities_text.__doc__)
    entities_text_parser.add_argument('text')

    entities_file_parser = subparsers.add_parser(
        'entities-file', help=entities_file.__doc__)
    entities_file_parser.add_argument('gcs_uri')

    syntax_text_parser = subparsers.add_parser(
        'syntax-text', help=syntax_text.__doc__)
    syntax_text_parser.add_argument('text')

    syntax_file_parser = subparsers.add_parser(
        'syntax-file', help=syntax_file.__doc__)
    syntax_file_parser.add_argument('gcs_uri')

    args = parser.parse_args()

    if args.command == 'sentiment-text':
        sentiment_text(args.text)
    elif args.command == 'sentiment-file':
        sentiment_file(args.gcs_uri)
    elif args.command == 'entities-text':
        entities_text(args.text)
    elif args.command == 'entities-file':
        entities_file(args.gcs_uri)
    elif args.command == 'syntax-text':
        syntax_text(args.text)
    elif args.command == 'syntax-file':
        syntax_file(args.gcs_uri)
    elif args.command == 'sentiment-entities-text':
        entity_sentiment_text(args.text)
    elif args.command == 'sentiment-entities-file':
        entity_sentiment_file(args.gcs_uri)
