# Meetup auto-reminder

:warning: This integration is no longer working due to removal
of API keys feature at meetup.com. :warning:

A simple piece of software posting a summary of upcoming meetups to a Slack channel.

Intended to run on [AWS Lambda](http://docs.aws.amazon.com/lambda/latest/dg/welcome.html), using [Serverless](https://serverless.com/)

## Capra setup

Capra internal details: https://confluence.capraconsulting.no/x/kINGBw

### Configuration

Two elements in Parameter Store:

* `/meetup-reminder/prod/meetup-api-key` - API key for meetup.com
* `/meetup-reminder/prod/slack-webhook-url` - Slack webhook URL

### Deploying (Capra setup)

:warning: This stack is currently deleted and not in use. :warning:

Install Serverless globally:

```bash
npm install serverless -g
```

Install Serverless dependencies:

```bash
npm install
```

Install Python venv and activate:

```bash
# use python3 if python refers to python 2
python -m venv venv
source venv/bin/activate
```

Activate AWS credentials (this depends on your setup):

```bash
aws-vault exec capra
```

Verify account (assumes you have aws cli installed):

```bash
aws sts get-caller-identity
```

Account ID should be 923402097046.

Deploy template:

```bash
serverless deploy --verbose
```
