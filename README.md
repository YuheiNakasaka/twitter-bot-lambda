# twitter-bot-lambda

Create Twitter bot for a few minute!

# Requirements

- Python2.7(may be work in 3.x)
- virtualenv
- AWS Account
- aws cli
  - credentials and region
- Twitter Account
- Twitter App
  - COUNSUMER_KEY and CONSUMER_SECRET
  - ACCESS_TOKEN and ACCESS_TOKEN_SECRET

# USAGE

## 1) Setup AWS Account Id, IAM role(has AWSLambdaBasicExecutionRole), AWS Region, Twitter CONSUMER_KEY/ CONSUMER_SECRET/ACCESS_TOKEN/ACCESS_TOKEN_SECRET to .env file

Example of .env

```
# AWS Account ID
AWS_ACCOUNT_ID=12345678910
AWS_IAM_ROLE_NAME=lambda_basic_execution
AWS_REGION_NAME=ap-northeast-1

# Twitter app consumer key, consumer secret
CONSUMER_KEY=YOUR_COSUMER_KEY
CONSUMER_SECRET=YOUR_CONSUMER_SECRET

# tokens
ACCESS_TOKEN=YOUR_ACCESS_TOKEN
ACCESS_TOKEN_SECRET=YOUR_ACCESS_TOKEN_SECRET

```

## 2) pip install

```
$ pip install -q -t ./lib -r ./requirements.txt
```

## 3) Set up bot project

```
$ python setup.py
Account Name:your_twitter_bot_name
```

## 4) Upload and Scheduling

```
$ python deploy.py
Account Name:your_twitter_bot_name
Upload?(y/n):y
Shedule?(y/n):y
```

Done!

In default, this bot tweets per 30 minutes.
