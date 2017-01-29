#!/usr/bin/python
#-*- coding: utf-8 -*-
# library用にパスを追加しておく
import sys
sys.path.append('./lib')

import random
import re
import time
from datetime import datetime
import os
from os.path import join, dirname
from dotenv import load_dotenv
import tweepy
import pytz
from datetime import datetime,timedelta

# 定数
REFOLLOW_LIMIT = 5
REFOLLOW_HOUR = 12

# 環境変数を読み出す
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# メインのlambda function
def lambda_handler(event, context):
    print('Start to function')
    client = _get_client()
    tweet(client)
    # refollow(client)
    return 'success'

# ツイート実行
def tweet(client):
    now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    text = u"現在は{}です".format(now)
    client.update_status(status=text)

# gifmagazineからツイートを選んでリツイート実行
def retweet(client, tweet):
    if tweet.retweeted == False:
        client.retweet(tweet.id)

# gifmagazineからツイートを選んでいいね実行
def favorite(client, tweet):
    if tweet.favorited == False:
        client.create_favorite(tweet.id)

# 12時に1日1回フォロー返しをする
def refollow(client):
    jst = pytz.timezone('Asia/Tokyo')
    jst_now = datetime.now(jst)
    hour = jst_now.strftime("%H")
    if int(hour) == REFOLLOW_HOUR:
        my_followers = _get_my_followers(client)
        follower_ids = [follower.id for follower in my_followers]
        relationships = client.lookup_friendships(follower_ids)
        for relationship in relationships:
            if not relationship.is_following:
                client.create_friendship(relationship.id, True)
                time.sleep(2)

# 認証してクライアント作成
def _get_client():
    consumer_key = os.environ.get("CONSUMER_KEY")
    consumer_secret = os.environ.get("CONSUMER_SECRET")
    access_token = os.environ.get("ACCESS_TOKEN")
    access_token_secret = os.environ.get("ACCESS_TOKEN_SECRET")
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    client = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    return client

# 自分のフォロワーをできるだけ取得
def _get_my_followers(client):
    my_followers = []
    for follower in tweepy.Cursor(client.followers).items():
        my_followers.append(follower)
        if len(my_followers) > REFOLLOW_LIMIT:
            break
    return  my_followers
