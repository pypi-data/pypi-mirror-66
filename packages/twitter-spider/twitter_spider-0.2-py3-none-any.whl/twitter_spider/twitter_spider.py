# -*- coding: utf-8 -*-
from urllib.parse import urlencode
from time import sleep
import requests
import logging
import json
import csv

TWEETS_QUERY_PARAM = {
      "include_profile_interstitial_type": "1",
      "include_blocking": "1",
      "include_blocked_by": "1",
      "include_followed_by": "1",
      "include_want_retweets": "1",
      "include_mute_edge": "1",
      "include_can_dm": "1",
      "include_can_media_tag": "1",
      "skip_status": "1",
      "cards_platform": "Web-12",
      "include_cards": "1",
      "include_composer_source": True,
      "include_ext_alt_text": True,
      "include_reply_count": "1",
      "tweet_mode": "extended",
      "include_entities": True,
      "include_user_entities": True,
      "include_ext_media_color": True,
      "include_ext_media_availability": True,
      "send_error_codes": True,
      "simple_quoted_tweets": True,
      "include_tweet_replies": True,
      "count": "20",
      "ext": "mediaStats,highlightedLabel,cameraMoment"
}

class TwitterSpider:

    __headers = {
        "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
        "x-twitter-active-user": "yes",
        "x-twitter-client-language": "en"
    }

    __tweets_url = "https://api.twitter.com/2/timeline/profile/%s.json?%s"

    def __init__(
        self,
        csrf_token: str,
        guest_token: str,
        username: str,
        tweets_limit: int = 0,
        request_delay: int = 2,
        retweets: bool = False
    ):
        self.username = username
        self.req_session = requests.Session()
        self.scraped_tweets = 0
        self.tweets_limit = tweets_limit
        self.request_delay = request_delay
        self.retweets = retweets

        self.__headers["x-csrf-token"] = csrf_token
        self.__headers["x-guest-token"] = guest_token

        out_file = open(
            "%s.csv" % username, 
            'w+', 
            newline='\n', 
            encoding='utf-8'
        )

        self.csv_wr = csv.writer(out_file, quoting=csv.QUOTE_ALL)
        self.csv_wr.writerow([
            "Full text",
            "reply_count",
            "favorite_count",
            "retweet_count",
            "created_at"
        ])

        self.tweets_query_params = TWEETS_QUERY_PARAM

    @property
    def username_to_user_id(self):
        """
        Returns the twitter user id from username
        """
        query_params = {
            "variables": {
                "screen_name": self.username,
                "withHighlightedLabel": True
            }
        }

        user_id_url = "https://api.twitter.com/graphql/P8ph10GzBbdMqWZxulqCfA/UserByScreenName?%s" % (
            urlencode(query_params)
        )

        #Replace single qoutes with double qoutes
        user_id_url = user_id_url.replace("%27", "%22")

        #Request only accepts lower case True value
        user_id_url = user_id_url.replace("True", "true")

        resp = self.req_session.get(
            url = user_id_url,
            headers = self.__headers
        )

        try:
            user_id = resp.json()['data']['user']['rest_id']
        except Exception as e:
            print(e)
            return

        print("Got ID for username='%s', user_id='%s'" % (
            self.username, user_id)
        )

        return user_id

    def get_tweets(self, userId: str, nextCursor: str = None):
        self.tweets_query_params['userId'] = userId

        """
        Twitter uses cursors as pagination.
        If a cursor has been found, it is being added to the 
        query string parameters
        """
        if nextCursor:
            self.tweets_query_params['cursor'] = nextCursor

        tweets_list_url = self.__tweets_url % (
            self.tweets_query_params['userId'],
            urlencode(self.tweets_query_params)
        )

        resp = self.req_session.get(
            url = tweets_list_url,
            headers = self.__headers
        )

        try:
            tweets = resp.json()['globalObjects']['tweets']
        except Exception as e:
            print(e, "was not found")
            return

        """
        Parsing tweets
        """
        for ind, tweet in enumerate(tweets):
            if not self.retweets:
                if self.tweets_query_params['userId'] != tweets[tweet]["user_id_str"]:
                    continue

            self.csv_wr.writerow([
                tweets[tweet]["full_text"],
                tweets[tweet]["reply_count"],
                tweets[tweet]["favorite_count"],
                tweets[tweet]["retweet_count"],
                tweets[tweet]["created_at"]
            ])
            print("New tweet added with id: %s" % (
                tweets[tweet]['id_str'],)
            )

            self.scraped_tweets += 1

        """
        Searching for next page cursor id
        """
        entries = resp.json()['timeline']['instructions'][0]['addEntries']['entries']
        
        for entry in entries:
            try:
                cursor = entry['content']['operation']['cursor']
            except:
                continue

            if cursor['cursorType'] == "Bottom":
                nextCursor = cursor['value']
                print("Found new cursor: %s" % (nextCursor,))
                break

        if self.scraped_tweets >= self.tweets_limit and self.tweets_limit != 0:
            return
        else:
            if len(tweets) > 0 and nextCursor:
                sleep(self.request_delay)
                return self.get_tweets(userId, nextCursor)

            return