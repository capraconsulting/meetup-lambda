#!/usr/bin/env python3

import os
import requests

import time
import datetime

MEETUP_API_KEY = os.environ["MEETUP_API_KEY"]
SLACK_WEBHOOK_URL = os.environ["SLACK_WEBHOOK_URL"]

# Number of days to look for meetups to include in summary
UPCOMING_PERIOD = 14


def time_inside_desired_period(start_time, end_time):
    return lambda meetup: start_time < (meetup["time"] / 1000) < end_time


def format_meetup_info(meetup):
    formatted_date = datetime.date.fromtimestamp(
        meetup['time'] / 1000).strftime("%d.%m")
    return "{formatted_date}: <{link}|{name}>".format(
        formatted_date=formatted_date, **meetup)


def retrieve_upcoming_meetups(event=None, context=None):
    meetups = requests.get(
        "https://api.meetup.com/self/calendar",
        params={"sign": "true",
                "key": MEETUP_API_KEY},
        headers={"Accept": "application/json"}).json()

    start_time = time.time()
    end_time = start_time + (3600 * 24 * UPCOMING_PERIOD)

    meetups_in_desired_period = filter(
        time_inside_desired_period(start_time, end_time), meetups)
    # print(json.dumps(meetups))

    meetup_list_text = "\n".join(
        map(format_meetup_info, meetups_in_desired_period))

    message_body = """Alle elsker meetups! Her er en oversikt over meetups de neste to ukene:

{meetup_list}

Ta med en venn, ta med to, meetups er gøy!
    """.format(meetup_list=meetup_list_text)

    requests.post(SLACK_WEBHOOK_URL, json={"text": message_body})
    print("Message sent")
    print(message_body)


if __name__ == "__main__":
    retrieve_upcoming_meetups()
