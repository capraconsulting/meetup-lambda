#!/usr/bin/env python3

import datetime
import json
import logging
import os
import time

import requests

MEETUP_API_KEY = os.environ["MEETUP_API_KEY"]
SLACK_WEBHOOK_URL = os.environ["SLACK_WEBHOOK_URL"]

# Number of days to look for meetups to include in summary
UPCOMING_PERIOD = 14

logger = logging.getLogger("meetup")
logger.setLevel(logging.DEBUG)


def time_inside_desired_period(start_time, end_time):
    return lambda meetup: start_time < (meetup["time"] / 1000) < end_time


def format_meetup_info(meetup):
    formatted_date = datetime.date.fromtimestamp(meetup["time"] / 1000).strftime(
        "%d.%m"
    )
    return "{formatted_date}: <{link}|{name}>".format(
        formatted_date=formatted_date, **meetup
    )


def retrieve_upcoming_meetups():
    response = requests.get(
        "https://api.meetup.com/self/calendar",
        params={"sign": "true", "key": MEETUP_API_KEY},
        headers={"Accept": "application/json"},
    )

    try:
        response.raise_for_status()
    except Exception:
        logger.debug(f"Content received: {response.content}")
        raise

    meetups = response.json()
    logger.debug(f"Data received: {json.dumps(meetups)}")

    start_time = time.time()
    end_time = start_time + (3600 * 24 * UPCOMING_PERIOD)

    meetups_in_desired_period = filter(
        time_inside_desired_period(start_time, end_time), meetups
    )

    return meetups_in_desired_period


def post_slack(message):
    logger.debug(f"Sending message to Slack: {message}")
    requests.post(SLACK_WEBHOOK_URL, json={"text": message})


def main():
    upcoming = None
    try:
        upcoming = retrieve_upcoming_meetups()
    except Exception:
        post_slack(
            """I failed to retrieve the latest list of meetups. Please check my logs!

https://github.com/capraconsulting/meetup-lambda"""
        )
        raise

    meetup_list_text = "\n".join(map(format_meetup_info, upcoming))

    message_body = f"""Alle elsker meetups! Her er en oversikt over meetups de neste to ukene:

{meetup_list_text}

Ta med en venn, ta med to, meetups er gøy!
https://github.com/capraconsulting/meetup-lambda"""

    post_slack(message_body)


def lambda_handler(event=None, context=None):
    main()


if __name__ == "__main__":
    main()
