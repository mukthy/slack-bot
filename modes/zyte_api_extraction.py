import requests
import time
import json
from slack import WebClient
from slack_sdk import WebClient
import os
from dotenv import load_dotenv
from pathlib import Path


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


def zapi_extraction(url, user, slack_webhook_url, headers, page_type):
    payload = json.dumps({
        "url": f"{url}",
        f"{page_type}": True,
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
    if response.status_code == 200:

        print(zyte_api_result)
        with open(f"{user}.json", "w") as f:
            json.dump(zyte_api_result, f, indent=4)
            f.close()
        zyte_data_api_result = {
            "text": "ZyteAPI Extraction",
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"@{user} Zyte API {page_type} Extraction results for {url}:",
                    },
                }
            ],
        }
        zyte_resp = requests.post(
            url=slack_webhook_url,
            headers=headers,
            data=json.dumps(zyte_data_api_result),
        )
        file_upload = client.files_upload(
            channels="C02NY5ME01L",
            filetype="json",
            file=f"{user}.json",
            title=f"{url}",
            user=f"{user}",
        )
        print(file_upload.status_code)
        print(zyte_resp.status_code)
        time.sleep(2)
        os.remove(f"{user}.json")
        return zyte_resp
    else:
        zyte_data_api_result = {
            "text": "ZyteAPI Extraction",
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"@{user} Zyte API {page_type} Extraction results for {url}:",
                    },
                },
                {
                    "type": "section",
                    "block_id": "section567",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"Seems like a Ban! \n\n Reach out to #zapi-support team. \n\n The Result is given below: \n\n {zyte_api_result}",
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
