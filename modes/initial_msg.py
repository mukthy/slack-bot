import requests
import json


def initial_message(response_url, headers, user, task) -> requests.Response:
    payload = {
        "text": "Intercepted Requests",
        "blocks": [
            {
                "type": "section",
                "block_id": "section567",
                "text": {
                    "type": "mrkdwn",
                    "text": f"@{user} Please wait till ZyteBot Completes your {task}\n"
                },
            },
        ],
    }

    response = requests.post(url=response_url, headers=headers, data=json.dumps(payload))
    return response


def incorrect_format(response_url, headers, user) -> requests.Response:
    payload = {
        "text": "Intercepted Requests",
        "blocks": [
            {
                "type": "section",
                "block_id": "section567",
                "text": {
                    "type": "mrkdwn",
                    "text": f"@{user} Please enter the correct format:\n `/zytebot-kibana 382142, amazon.com`\n"
                },
            },
        ],
    }

    response = requests.post(url=response_url, headers=headers, data=json.dumps(payload))
    return response
