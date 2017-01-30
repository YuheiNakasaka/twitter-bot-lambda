#!/usr/bin/python
#-*- coding: utf-8 -*-
import sys
sys.path.append('./lib')

import sys
import re
import subprocess
import os
from os.path import join, dirname
from dotenv import load_dotenv
import tweepy
import webbrowser

# 環境変数を読み出す
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# トークン取得からファイル更新までbotの設定をする
def bot_setup(account_name):
    # access token/secret等を設定する
    consumer_key = os.environ.get("CONSUMER_KEY")
    consumer_secret = os.environ.get("CONSUMER_SECRET")
    access_token = os.environ.get("ACCESS_TOKEN")
    access_token_secret = os.environ.get("ACCESS_TOKEN_SECRET")
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # lambda.jsonのfunction nameをacccount_name+botに変える
    # lambda.jsonのaccount_id部分を置換する
    # lambda.jsonのrole_name部分を置換する
    lambda_file_name = "./lambda.json".format(account_name=account_name)
    lambda_file = open(lambda_file_name)
    content = lambda_file.read()
    lambda_file.close()
    bot_name = "{}-bot".format(account_name)
    content = re.sub("twitter-bot-lambda", bot_name, content)
    aws_account_id = os.environ.get("AWS_ACCOUNT_ID")
    aws_iam_role_name = os.environ.get("AWS_IAM_ROLE_NAME")
    role_arn = "arn:aws:iam::{}:role/{}".format(aws_account_id, aws_iam_role_name)
    content = re.sub("YOUR_IAM_ROLE", role_arn, content)
    aws_region = os.environ.get("AWS_REGION_NAME")
    content = re.sub("YOUR_REGION", aws_region, content)
    lambda_file = open(lambda_file_name, 'w')
    lambda_file.write(content)
    lambda_file.close()

    # twitterアカウントの設定
    client = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    _account_setup(client)

# twitterのアカウントの設定
def _account_setup(client):
    # 名前と自己紹介を設定
    new_account_name = u'時報君'
    description = u'時刻をお伝えします'
    client.update_profile(name=new_account_name.encode('utf8'), description=description.encode('utf8'))

    # プロフ画像を設定
    img_path = './mezamashidokei_character.png'
    client.update_profile_image(img_path)

# アカウント名取得
account_name = os.environ.get("TWITTER_ACCOUNT_NAME")
if account_name is None or re.search("^[0-9a-zA-Z_]{1,15}$", account_name) is None:
    print("Error: Account Name is invalid!")
    exit()

# 各種実行
print("====== Start to generate bot project ======")
bot_setup(account_name)
print("Successfuly generated bot project!")
