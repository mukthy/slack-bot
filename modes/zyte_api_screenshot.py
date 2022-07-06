import requests
import time
import json
from slack import WebClient
from slack_sdk import WebClient
import os
from dotenv import load_dotenv
from pathlib import Path
import base64


def initial_message(response_url, user):
    initial_msg = {
        "text": f"@{user} It may take upto 5 mins to complete, Go for a break or listen to a song :sweat_smile: "
    }
    initial_response = requests.post(
        url=response_url, json=initial_msg)
    return initial_response


env_path = Path(".", ".") / ".env"
print(env_path)
load_dotenv(dotenv_path=env_path)
zyte_api = os.environ['ZYTE_DATA_API']
zyte_api_url = os.environ['ZYTE_DATA_API_URL']
client = WebClient(token=os.environ["SLACK_TOKEN"])
channel_id = os.environ['CHANNEL_ID']


def zyte_api_screenshot(url, user, slack_webhook_url, headers):
    payload = json.dumps({
        "url": f"{url}",
        "browserHtml": True,
        "javascript": True,
        "httpResponseHeaders": True,
        "screenshot": True,
        "screenshotOptions": {
            "fullPage": True,
        },
        "actions": [
            {
                "timeout": 10,
                "action": "waitForTimeout"
            }],
    })

    header = {
        'Content-Type': 'application/json'
    }

    response = requests.post(
        zyte_api_url,
        auth=(zyte_api, ""),
        headers=header,
        data=payload,
    )
    zyte_api_result = response.json()
    if "screenshot" in zyte_api_result:

        print(zyte_api_result["screenshot"])
        # f = open(f"{user}.html", "w")
        # f.write(zyte_api_result["browserHtml"])
        # f.close()
        img_data = bytes(zyte_api_result["screenshot"], "utf-8")
        with open(f"{user}.png", "wb") as fh:
            fh.write(base64.decodebytes(img_data))

        zyte_api_result = {
            "text": "Antibot Details",
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"@{user} Zyte Data API Screenshot for {url}",
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
        zyte_resp = requests.post(
            url=slack_webhook_url,
            headers=headers,
            data=json.dumps(zyte_api_result),
        )
        file_upload = client.files_upload(
            channels=f"{channel_id}",
            filetype="png",
            file=f"{user}.png",
            title=f"{url}",
            user=f"{user}",
        )
        print(file_upload.status_code)
        print(zyte_resp.status_code)
        time.sleep(3)
        os.remove(f"{user}.png")
        print(f'{user}.png has been removed!')
        return zyte_resp

    else:
        zyte_data_api_result = {
            "text": "Zyte Data API Screenshot",
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"@{user} Zyte Data API results for {url}:",
                    },
                },
                {
                    "type": "section",
                    "block_id": "section567",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"Seems like a Ban! \n\n Reach out to #uncork team. \n\n The Result is given below: \n\n {zyte_api_result}",
                    },
                },
            ],
        }
        zyte_resp = requests.post(
            url=slack_webhook_url,
            headers=headers,
            data=json.dumps(zyte_data_api_result),
        )
        return zyte_resp
