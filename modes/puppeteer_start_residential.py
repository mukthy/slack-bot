import json
import signal
import subprocess
import time

import psutil
from slack_sdk import WebClient
import os
from dotenv import load_dotenv
from pathlib import Path
import requests


def initial_message(response_url, user):
    initial_msg = {
        "text": f"@{user} Give me a min Fetching results :sweat_smile: "
    }
    initial_response = requests.post(
        url=response_url, json=initial_msg)
    return initial_response


env_path = Path("..") / ".env"
print(env_path)
load_dotenv(dotenv_path=env_path)
client = WebClient(token=os.environ["SLACK_TOKEN"])
channel_id = os.environ['CHANNEL_ID']


def start(url, user, slack_webhook_url, headers, response_url):
    out = subprocess.Popen(['node', '/home/mukthy/nodes_programs/puppeteer_dc.js', f'{url}', f'{user}.png'],
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    stdout, stderr = out.communicate()

    print(stdout)
    print(stderr)
    print(out.pid)
    process = psutil.pid_exists(out.pid)
    print(process)

    if process:
        os.kill(out.pid, signal.SIGTERM)

    else:
        print(f'{process} is closed')

    puppeteer_result = {
        "text": "Zyte Smartproxy Puppeteer Details",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"@{user} Zyte Smartproxy Puppeteer Residential screenshot for {url} is given below: \n",
                },
            },
            # {
            #     "type": "section",
            #     "block_id": "section567",
            #     "text": {
            #         "type": "mrkdwn",
            #         "text": f"The Result is given below: \n\n {final_result}"
            #     },
            # },
        ],
    }
    puppeteer_resp = requests.post(
        url=slack_webhook_url,
        headers=headers,
        data=json.dumps(puppeteer_result),
    )

    file_upload = client.files_upload(
        channels=f"{channel_id}",
        filetype="png",
        file=f"{user}.png",
        title=f"{url}",
        user=f"{user}",
    )

    print(file_upload.status_code)
    print(puppeteer_resp.status_code)
    time.sleep(3)
    os.remove(f"{user}.png")
    print(f'{user}.png has been removed!')
    return puppeteer_resp

#
# start()

