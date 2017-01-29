#!/usr/bin/python
#-*- coding: utf-8 -*-

import os
import re
import random
import subprocess
from os.path import join, dirname
from dotenv import load_dotenv

# AWS Lambdaにデプロイを行う
def upload():
    deploy_cmd = "lambda-uploader  ./ --config ./lambda.json"

    # 実行
    try:
        subprocess.check_call(deploy_cmd, shell=True)
    except Exception as e:
        print(e)

# CloudWatchのcron設定をする
def schedule_setup(account_name):
    # 環境変数を読み出す
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)
    aws_account_id = os.environ.get("AWS_ACCOUNT_ID")
    aws_region_name = os.environ.get("AWS_REGION_NAME")

    # すでにschedule ruleがある場合再設定はしない
    check_cmd = "aws events list-rules --name-suffix '{}-bot'".format(account_name)
    process = subprocess.Popen(check_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, _ = process.communicate()
    m = re.search("cron\((.+)\)", stdout)
    if m is None:
        # - 1) lambdaの関数実行権限をCloudWatchに与える
        cmd1 = "aws lambda add-permission --function-name \"{account_name}-bot\" --statement-id \"MySecureString\" --action 'lambda:InvokeFunction' --principal events.amazonaws.com --source-arn arn:aws:events:{aws_region_name}:{aws_account_id}:rule/{account_name}-bot".format(account_name=account_name, aws_account_id=aws_account_id, aws_region_name=aws_region_name)

        # - 2) Scheduleを作成する
        cmd2 = "aws events put-rule --name \"{account_name}-bot\" --schedule-expression \"cron(0/30 * * * ? *)\" --state ENABLED".format(account_name=account_name)

        # - 3) ScheduleをLambda関数に割り当てる
        cmd3 = "aws events put-targets --rule \"{account_name}-bot\" --targets Arn=arn:aws:lambda:{aws_region_name}:{aws_account_id}:function:{account_name}-bot,Id={account_name}-bot".format(account_name=account_name, aws_account_id=aws_account_id, aws_region_name=aws_region_name)

        # 順次実行
        try:
            subprocess.check_call(cmd1, shell=True)
            subprocess.check_call(cmd2, shell=True)
            subprocess.check_call(cmd3, shell=True)
        except Exception as e:
            print(e)

# アカウント名取得
account_name = raw_input('Account Name:')
if account_name is None or re.search("^[0-9a-zA-Z_]{1,15}$", account_name) is None:
    print("Error: Account Name is invalid!")
    exit()

# 実行するタスクを選択
do_upload = raw_input('Upload?(y/n):')
do_schedule = raw_input('Schedule?(y/n):')

# 各種実行
print("====== Start to deploy bot project ======")
dynamodb_setup(account_name)
if do_upload == 'y':
    upload(account_name)
if do_schedule == 'y':
    schedule_setup(account_name)
print("Successfuly deployed bot project!")
