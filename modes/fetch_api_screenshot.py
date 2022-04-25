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
    initial_response = requests.post(url=response_url, json=initial_msg)
    return initial_response


env_path = Path(".", ".") / ".env"
print(env_path)
load_dotenv(dotenv_path=env_path)
fetch_api = os.environ["FETCH_API"]
fetch_api_url = os.environ["FETCH_API_URL"]
client = WebClient(token=os.environ["SLACK_TOKEN"])
channel_id = os.environ["CHANNEL_ID"]


def fetch_api_req(url, user, slack_webhook_url, headers):
    response = requests.post(
        fetch_api_url,
        auth=(fetch_api, ""),
        json={
            "url": f"{url}",
            "render": True,
            "screenshot": True,
            "screenshot_options": {"full_page": True},
        },
    )
    fetch_api_result = response.json()
    if "screenshot" in fetch_api_result:

        print(fetch_api_result["screenshot"])
        # f = open(f"{user}.html", "w")
        # f.write(zyte_api_result["browserHtml"])
        # f.close()
        img_data = bytes(fetch_api_result["screenshot"], "utf-8")
        with open(f"{user}.png", "wb") as fh:
            fh.write(base64.decodebytes(img_data))

        fetch_api_result = {
            "text": "Antibot Details",
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"@{user} Fetch API results for {url} \n\n This netloc works with BrowserStack=Default, wait_for_timeout=3000, skip_trackers=False:",
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
            url=slack_webhook_url, headers=headers, data=json.dumps(fetch_api_result),
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
        print(f"{user}.png has been removed!")
        return zyte_resp

    elif "screenshot" not in fetch_api_result:

        response = requests.post(
            fetch_api_url,
            auth=(fetch_api, ""),
            json={
                "url": f"{url}",
                "render": True,
                "screenshot": True,
                "screenshot_options": {"full_page": True},
                "parameters": {
                    "navigation_timeout": 20000,
                    "goto_wait_until": "load",
                    "skip_trackers": False,
                    "wait_for_timeout": 3000,
                    "browserstack": "FIREFOX_HEADFUL_LINUX",
                },
            },
        )
        fetch_api_result = response.json()
        print(fetch_api_result)
        # f = open(f"{user}.html", "w")
        # f.write(zyte_api_result["browserHtml"])
        # f.close()
        if "screenshot" in fetch_api_result:
            img_data = bytes(fetch_api_result["screenshot"], "utf-8")
            with open(f"{user}.png", "wb") as fh:
                fh.write(base64.decodebytes(img_data))

            fetch_api_result = {
                "text": "Antibot Details",
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"@{user} Fetch API results for {url} \n\n This netloc works with BrowserStack=FIREFOX, wait_for_timeout=3000, skip_trackers=False:",
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
                data=json.dumps(fetch_api_result),
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
            print(f"{user}.png has been removed!")
            return zyte_resp

        else:
            response = requests.post(
                fetch_api_url,
                auth=(fetch_api, ""),
                json={
                    "url": f"{url}",
                    "render": True,
                    "screenshot": True,
                    "screenshot_options": {"full_page": True},
                    "parameters": {
                        "navigation_timeout": 20000,
                        "goto_wait_until": "load",
                        "skip_trackers": False,
                        "wait_for_timeout": 3000,
                        "browserstack": "CHROME_HEADFUL_LINUX",
                    },
                },
            )
            fetch_api_result = response.json()
            print(fetch_api_result)
            # f = open(f"{user}.html", "w")
            # f.write(zyte_api_result["browserHtml"])
            # f.close()
            if "screenshot" in fetch_api_result:
                img_data = bytes(fetch_api_result["screenshot"], "utf-8")
                with open(f"{user}.png", "wb") as fh:
                    fh.write(base64.decodebytes(img_data))

                fetch_api_result = {
                    "text": "Antibot Details",
                    "blocks": [
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": f"@{user} Fetch API results for {url} \n\n This netloc works with BrowserStack=CHROME, wait_for_timeout=3000, skip_trackers=False:",
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
                    data=json.dumps(fetch_api_result),
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
                print(f"{user}.png has been removed!")
                return zyte_resp

            else:
                fetch_api_result = {
                    "text": "Antibot Details",
                    "blocks": [
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": f"@{user} FetchAPI results for {url}:",
                            },
                        },
                        {
                            "type": "section",
                            "block_id": "section567",
                            "text": {
                                "type": "mrkdwn",
                                "text": f"Seems like a Ban! \n\n Reach out to #smartbrowser-support or troubleshoot manually. \n\n The Result is given below: \n\n {fetch_api_result}",
                            },
                        },
                    ],
                }
                fetch_resp = requests.post(
                    url=slack_webhook_url, headers=headers, data=json.dumps(fetch_api_result),
                )
                return fetch_resp
