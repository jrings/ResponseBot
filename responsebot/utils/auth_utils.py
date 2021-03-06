# Copyright 2016 Invisible Institute
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

"""
Utilities for authentication & authorization
"""
from __future__ import absolute_import

import logging

import tweepy
from tweepy.error import TweepError, RateLimitError

from responsebot.common.exceptions import AuthenticationError, APIQuotaError
from responsebot.responsebot_client import ResponseBotClient


def auth(config):
    """
    Perform authentication with Twitter and return a client instance to communicate with Twitter

    :param config: ResponseBot config
    :type config: :class:`~responsebot.utils.config_utils.ResponseBotConfig`
    :return: client instance to execute twitter action
    :rtype: :class:`~responsebot.responsebot_client.ResponseBotClient`
    :raises: :class:`~responsebot.common.exceptions.AuthenticationError`: If failed to authenticate
    :raises: :class:`~responsebot.common.exceptions.APIQuotaError`: If API call rate reached limit
    """
    auth = tweepy.OAuthHandler(config.get('consumer_key'), config.get('consumer_secret'))
    auth.set_access_token(config.get('token_key'), config.get('token_secret'))

    api = tweepy.API(auth)
    try:
        api.verify_credentials()
    except RateLimitError as e:
        raise APIQuotaError(e.args[0][0]['message'])
    except TweepError as e:
        raise AuthenticationError(e.args[0][0]['message'])
    else:
        logging.info('Successfully authenticated as %s' % api.me().screen_name)

        return ResponseBotClient(config=config, client=api)
