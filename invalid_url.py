import requests
import json


def check_url(user, response_url, headers):

    incorrect_url_message = {
        "text": "Antibot Details",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"@{user} Please enter a proper URL: https://example.com or http://example.com",
                },
            },
        ],
    }
    resp = requests.post(
        url=response_url, headers=headers, data=json.dumps(incorrect_url_message)
    )
    return resp
