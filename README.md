# twitter-bot-lambda

Create Twitter bot for a minute!

# Requirements

- Python2.7(may be work in 3.x)
- virtualenv
- AWS Account
- aws cli
  - credentials and region

# USAGE

## 1) Setup AWS Account Id and IAM role(has AWSLambdaBasicExecutionRole) to .env file

Example of .env

```
# AWS Account ID
AWS_ACCOUNT_ID=12345678910
AWS_IAM_ROLE_NAME=lambda_basic_execution
AWS_REGION_NAME=ap-northeast-1

...
```

## 2) Set up bot project

```
$ python setup.py
Account Name:your_twitter_bot_name
```

## 3) Upload and Scheduling

```
$ python deploy.py
Account Name:your_twitter_bot_name
Upload?(y/n):y
Shedule?(y/n):y
```

Done!

In default, this bot tweets per 30 minutes.
