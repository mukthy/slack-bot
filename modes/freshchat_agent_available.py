import requests
import json
from pathlib import Path
from dotenv import load_dotenv
import os
import pprint

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

freshchatauth = os.environ["FRESHCHATAUTH"]
apiurl = os.environ["APIURL"]


def check_agent_availability():
    payload = ""
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {freshchatauth}'
    }

    response = requests.request("GET", url=apiurl, headers=headers, data=payload)
    data = json.loads(response.text)
    data_len = len(data['agents'])
    # print(data_len)

    agents = []
    for i in range(data_len):
        if data['agents'][i]['availability_status'] == 'AVAILABLE':
            agents.append(data['agents'][i]['first_name'])
            # print(agents)

    print(len(agents))

    if len(agents) < 1:
        # print("No agents available")
        return "No agents"
    else:
        return agents


def post_results(user, headers, response_url, agent_results):
    post_message = {
        "text": "Freshchat Agents Results",
        "blocks": [
            {
                "type": "section",
                "block_id": "section567",
                "text": {
                    "type": "mrkdwn",
                    "text": f"@{user}:\n{agent_results} is/are available"
                },
            },
        ],
    }

    response = requests.post(
        url=response_url, headers=headers, data=json.dumps(
            post_message)
    )
    return response
