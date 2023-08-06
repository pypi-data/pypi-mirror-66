##!/usr/bin/env python3
# EX04 PCL2
# vihaus & ljovan
# Vincent Hauser & Luka Jovanovic

import re
from nltk.corpus import stopwords
import emoji
import cli


class Tweet:

    def __init__(self, tweet_str):
        self.orig_text = tweet_str
        # remove "Variation Selector-16" (not matched by emoji library)
        self.orig_text = self.orig_text.replace('\ufe0f', '')
        self.preprocessed_tokens = None

    def get_preprocessed_text(self):
        return ' '.join(self.preprocessed_tokens)

    def __repr__(self):
        return "<Tweet '{}'>".format(self.get_preprocessed_text())


class TweetProcessor:

    ANONYMOUS_MENTION = "@MENTION"

    _token_pattern = r"[\w@#]+|[.,!?;:'()–\-&]|\S+"
    _url_pattern = r"\b(?:https?://)?[\w\-]+\.\w[\w/.\-~%?=&]+"

    def __init__(self):
        """ prepend emoji and url regex to match them as single tokens """
        self._token_pattern = (
            emoji.get_emoji_regexp().pattern.strip('()')
            + '|' + self._url_pattern
            + '|' + self._token_pattern
        )

    def preprocess(self, tweet_str: str) -> Tweet:
        """ Preprocesses a tweet and returns the result. """
        tweet = Tweet(tweet_str)
        self._tokenize(tweet)
        self._remove_urls(tweet)
        self._remove_emojis(tweet)
        self._remove_hashtags(tweet)
        self._anonymize_mentions(tweet)
        return tweet

    def cli_preprocess(self, tweet_str: str) -> Tweet:
        """ Function used in combination with cli.py flags"""
        tweet = Tweet(tweet_str)
        self._tokenize(tweet)
        if cli.user_flag.url_bool == False:
            self._remove_urls(tweet)
        if cli.user_flag.emoji_bool == False:
            self._remove_emojis(tweet)
        if cli.user_flag.hashtag_bool == False:
            self._remove_hashtags(tweet)
        if cli.user_flag.anonymize_bool == False:
            self._anonymize_mentions(tweet)
        return tweet


    def _tokenize(self, tweet: Tweet):
        """ Stores a tokenized version in the tweet. """
        tokens = re.findall(self._token_pattern, tweet.orig_text)
        tweet.preprocessed_tokens = tokens

    def _remove_hashtags(self, tweet: Tweet):
        """ Removes hashtags from the tokenized tweet. """
        tweet.preprocessed_tokens = [
            token for token in tweet.preprocessed_tokens
            if not token.startswith('#')
        ]

    def _remove_urls(self, tweet: Tweet):
        """ Removes urls from the tokenized tweet. """
        tweet.preprocessed_tokens = [
            token for token in tweet.preprocessed_tokens
            if not re.match(self._url_pattern, token)
        ]

    def _anonymize_mentions(self, tweet: Tweet):
        """ Anonymizes mentions in the tokenized tweet. """
        tweet.preprocessed_tokens = [
            self.ANONYMOUS_MENTION if token.startswith('@') else token
            for token in tweet.preprocessed_tokens
        ]

    def _remove_emojis(self, tweet: Tweet):
        """ Removes emojis from the tokenized tweet. """
        tweet.preprocessed_tokens = [
            token for token in tweet.preprocessed_tokens
            if token not in emoji.UNICODE_EMOJI
        ]


class EnTPP(TweetProcessor):

    _stopwords_set = set(stopwords.words('english'))

    def preprocess(self, tweet_str: str) -> Tweet:
        tweet = super().preprocess(tweet_str)
        self._remove_stopwords(tweet)
        return tweet

    def cli_preprocess(self, tweet_str: str) -> Tweet:
        """Function used in combination for cli.py flags"""
        tweet = super().cli_preprocess(tweet_str)
        if cli.user_flag().stopwords_bool == False:
            self._remove_stopwords(tweet)
        return tweet

    def _remove_stopwords(self, tweet: Tweet):
        """Removes stopwords from the tokenized tweet."""
        tweet.preprocessed_tokens = [
            token for token in tweet.preprocessed_tokens
            if token not in self._stopwords_set
        ]


class EsTPP(TweetProcessor):
    """ modify tokenization to respect Spanish punctuation marks. """
    _token_pattern = r"[\w@#]+|[.,!¡?¿;:'()–\-&«»]"

