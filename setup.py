#!/usr/bin/python
#-*- coding: utf-8 -*-
import sys
import re
import subprocess
import os
from os.path import join, dirname
from dotenv import load_dotenv
import tweepy
import webbrowser

# ディレクトリ生成からpip installまでプロジェクト設定をする
def project_setup(account_name):
    # コマンド定義
    # pip install
    pip_intall_cmd   = "pip install -q -t ./lib -r ./requirements.txt".format(account_name=account_name)

    # コマンド実行。失敗すると例外が発生する。
    try:
        subprocess.check_call(pip_intall_cmd, shell=True)
    except Exception as e:
        print(e)

# トークン取得からファイル更新までbotの設定をする
def bot_setup(account_name):
    # 環境変数を読み出す
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)

    # access token/secretを取得する
    consumer_key = os.environ.get("CONSUMER_KEY")
    consumer_secret = os.environ.get("CONSUMER_SECRET")
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth_url = auth.get_authorization_url()
    webbrowser.open(auth_url)
    verifier = raw_input('Verifier:')
    auth.get_access_token(verifier)
    new_atoken = auth.access_token
    new_atoken_secret = auth.access_token_secret

    # envファイルのトークンを取得したものに置き換える
    env_file_name = "./.env".format(account_name=account_name)
    env_file = open(env_file_name)
    content = env_file.read()
    env_file.close()
    old_atoken = re.search("ACCESS_TOKEN=(.*)\n", content).group(1)
    old_atoken_secret = re.search("ACCESS_TOKEN_SECRET=(.*)\n", content).group(1)
    content = re.sub(old_atoken, new_atoken, content)
    content = re.sub(old_atoken_secret, new_atoken_secret, content)
    env_file = open(env_file_name, 'w')
    env_file.write(content)
    env_file.close()

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
    new_account_name = '時報君'
    description = '時刻をお伝えします'
    client.update_profile(name=new_account_name.encode('utf8'), description=description.encode('utf8'))

    # プロフ画像を設定
    img_path = './mezamashidokei_character.png'
    client.update_profile_image(img_path)

# アカウント名取得
account_name = raw_input('Account Name:')
if account_name is None or re.search("^[0-9a-zA-Z_]{1,15}$", account_name) is None:
    print("Error: Account Name is invalid!")
    exit()

# 各種実行
print("====== Start to generate bot project ======")
project_setup(account_name)
bot_setup(account_name)
print("Successfuly generated bot project!")
