import datetime
import time
from typing import Union, List, Any

import requests
import json
from pathlib import Path
from dotenv import load_dotenv
import os
from datetime import datetime
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

    # print('Current Time:', time.utc(time.time()))
    # print(result)
    if len(agents) > 0:
        result = "Freshdesk Agents Availability Live!" + "\n" + datetime.utcnow().strftime(
            "%Y-%m-%d %H:%M:%S") + " UTC" + " - " + str(agents)
        with open('/Users/mukthy/Desktop/office/slack_bots/slack-bot_dev/templates/agents.txt', 'w') as f:
            f.write(str(result))
        return result
    else:
        result = "Freshdesk Agents Availability Live!" + "\n" + datetime.utcnow().strftime(
            "%Y-%m-%d %H:%M:%S") + " UTC" + " - " + "No agents available at the moment!"
        with open('/Users/mukthy/Desktop/office/slack_bots/slack-bot_dev/templates/agents.txt', 'w') as f:
            f.write(str(result))
        return result

    # return agents


print(check_agent_availability())
