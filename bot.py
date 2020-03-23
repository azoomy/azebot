# import tweepy
# # from tweepy import StreamListener
# # import TB_credentials
# # from time import sleep
# #
# # auth = tweepy.OAuthHandler(TB_credentials.CONSUMER_KEY, TB_credentials.CONSUMER_SECRET)
# # auth.set_access_token(TB_credentials.ACCESS_TOKEN, TB_credentials.ACCESS_TOKEN_SECRET)
# #
# # api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
# # search = '#punintended'
# #
# # class MyStreamListener(StreamListener):
# #     def on_status(self, status):
# #         print(status)
# #     def on_error(self, status_code):
# #         print(status_code)
# #
# #
# # def LiandRet():
# #     for tweet in tweepy.Cursor(api.search, search).items():
# #         try:
# #             print("Tweet Liked")
# #             tweet.favorite()
# #         except tweepy.TweepError as e:
# #             print(e.reason)
# #         try:
# #             print("Tweet Retweeted")
# #             tweet.retweet()
# #         except tweepy.TweepError as e:
# #                 print(e.reason)
# #         except StopIteration:
# #             break
# #
# # myStreamListener = MyStreamListener()
# # myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
# # LiandRet()
# !/usr/bin/env python
# tweepy-bots/bots/favretweet.py

import tweepy
import logging
from config import create_api
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


class FavRetweetListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        self.me = api.me()

    def on_status(self, tweet):
        logger.info(f"Processing tweet id {tweet.id}")
        if tweet.in_reply_to_status_id is not None or \
                tweet.user.id == self.me.id:
            # This tweet is a reply or I'm its author so, ignore it
            return
        if not tweet.favorited:
            # Mark it as Liked, since we have not done it yet
            try:
                tweet.favorite()
            except Exception as e:
                logger.error("Error on fav", exc_info=True)
        if not tweet.retweeted:
            # Retweet, since we have not retweeted it yet
            try:
                tweet.retweet()
            except Exception as e:
                logger.error("Error on fav and retweet", exc_info=True)

    def on_error(self, status):
        logger.error(status)


def main(keyword):
    api = create_api()
    tweets_listener = FavRetweetListener(api)
    stream = tweepy.Stream(api.auth, tweets_listener)
    stream.filter(track=keyword, languages=["en"])

if __name__=="__main__":
    main(["pun intended"])