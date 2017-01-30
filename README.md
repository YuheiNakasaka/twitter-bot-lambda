# twitter-bot-lambda

Create Twitter bot for a few minute!

# Requirements

- Python2.7
- virtualenv
  - create virtual environment
    - https://virtualenv.readthedocs.org/en/latest/
- AWS Account
- aws cli
  - credentials and region
- Twitter Account
- Twitter App
  - CONSUMER_KEY and CONSUMER_SECRET
  - ACCESS_TOKEN and ACCESS_TOKEN_SECRET

# USAGE

## 1) Setup AWS Account Id, IAM role(has AWSLambdaBasicExecutionRole), AWS Region, Twitter CONSUMER_KEY/ CONSUMER_SECRET/ACCESS_TOKEN/ACCESS_TOKEN_SECRET to .env file

Example of .env

```
# AWS settings
AWS_ACCOUNT_ID=12345678910
AWS_IAM_ROLE_NAME=lambda_basic_execution
AWS_REGION_NAME=ap-northeast-1

# Twitter account name
TWITTER_ACCOUNT_NAME=yamadatarou01234

# Twitter app consumer key, consumer secret
CONSUMER_KEY=hogehoge01234
CONSUMER_SECRET=fugafuga01234

# Twitter account tokens
ACCESS_TOKEN=nyannyan01234
ACCESS_TOKEN_SECRET=wanwan01234

# [Options] Virtualenv path
CUSTOM_VENV_PATH=
```

## 2) pip install

```
$ pip install -q -t ./lib -r ./requirements.txt
```

## 3) Set up bot project

```
$ python setup.py
```

## 4) Upload and Scheduling

```
$ python deploy.py
Upload?(y/n):y
Shedule?(y/n):y
```

Done!

In default, this bot tweets per 30 minutes.

# Development

Run script with python-lambda-local.

```
$ python-lambda-local -f lambda_handler  ./tweet.py ./event.json
```

# Deploy

```
$ python deploy.py
Upload?(y/n):y
Shedule?(y/n):n
```
