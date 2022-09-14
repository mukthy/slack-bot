from typing import Union, List, Any

import requests
import json
from pathlib import Path
from dotenv import load_dotenv
import os
import pprint

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

mukapi = os.environ["MUKAPI"]
freshdeskagenturl = os.environ["FRESHDESK_AGENT_URL"]


def check_agent_availability() -> Union[list[Any], str]:
    agents = []
    for page in range(1, 3):
        freshdeskagent_full_url = f"{freshdeskagenturl}{page}"
        print(freshdeskagent_full_url)

        payload = {}
        headers = {
            'Content-Type': 'application/json',
        }

        response = requests.request("GET", url=freshdeskagent_full_url, headers=headers, auth=(mukapi, 'x'),
                                    data=payload)
        data = json.loads(response.text)
        # pprint.pprint(data[0]['available'])
        print(len(data))
        for i in range(len(data)):
            if data[i]['available']:
                # print(data[i]['contact']['name'])
                agents.append(data[i]['contact']['name'])

    if len(agents) > 0:
        return agents
    else:
        return "No agents"

    # return agents


def post_results(user, headers, response_url, freshdesk_agents_result):
    post_message = {
        "text": "Freshchat Agents Results",
        "blocks": [
            {
                "type": "section",
                "block_id": "section567",
                "text": {
                    "type": "mrkdwn",
                    "text": f"@{user}:\n{freshdesk_agents_result} is/are available on FreshDesk!"
                },
            },
        ],
    }

    response = requests.post(
        url=response_url, headers=headers, data=json.dumps(
            post_message)
    )
    return response
