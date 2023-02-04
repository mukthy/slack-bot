import requests
import json
from pathlib import Path
from dotenv import load_dotenv
import os
import pprint

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

mukapi = os.environ["MUKAPI"]
freshdeskcontacturl = os.environ["FRESHDESK_CONTACT_URL"]


def get_agent_id(email):
    url = f"{freshdeskcontacturl}"+"autocomplete?term="+f"{email}"

    payload = {}
    headers = {
        "content-type": "application/json",
    }

    try:
        response = requests.request("GET", url, auth=(mukapi, ''), headers=headers, data=payload)
        response = json.loads(response.text)
        # print(response)
        agent_id = response[0]["id"]
        print(agent_id)
        return agent_id

    except IndexError:
        print("No agent found with this email id")
        return None


def set_permission(agent_id):
    url = f"{freshdeskcontacturl}"+f"{agent_id}/make_agent"

    payload = json.dumps({
        "type": "support_agent",
        "ticket_scope": 2,
        "occasional": True,
        "group_ids": [
            22000159658,
            22000159659,
            22000160023,
            22000163057,
            22000163577,
            22000164209,
            22000164320,
            22000166705
        ],
        "role_ids": [
            22000161214
        ]
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("PUT", url, auth=(mukapi, ''), headers=headers, data=payload)

    data = json.loads(response.text)
    print(data)
    return response.status_code


# if __name__ == "__main__":
#     agent_id = get_agent_id("muktheeswaran.m@gmail.com")
#     set_permission(agent_id)

