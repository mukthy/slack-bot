import requests
import os
from dotenv import load_dotenv
from pathlib import Path
import threading
import json


def initial_message(response_url, user):

    starting_region_check = {
        "text": f"@{user} It may take upto 5 mins to complete, Go for a break or listen to a song :sweat_smile: "
    }
    initial_response = requests.post(
        url=response_url, json=starting_region_check)
    return initial_response


def post_result_to_slack(response_url, headers, url, user, ok_result, error_result):
    ok_result = json.dumps(ok_result)
    error_result = json.dumps(error_result)
    print(ok_result)
    print(error_result)
    region_check_results = {
        "text": "Antibot Details",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"@{user} Region-check results for {url}:",
                },
            },
            {
                "type": "section",
                "block_id": "section567",
                "text": {
                    "type": "mrkdwn",
                    "text": f"200 OK Results: \n {ok_result} \n\n Results with Errors: \n {error_result}",
                },
            },
        ],
    }
    post_result_to_slack = requests.post(
        url=response_url,
        headers=headers,
        data=json.dumps(region_check_results),
    )
    return post_result_to_slack
