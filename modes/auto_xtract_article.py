import requests
import json
import os
from dotenv import load_dotenv
from pathlib import Path
import time
from slack_sdk import WebClient

env_path = Path(".", ".") / ".env"
load_dotenv(dotenv_path=env_path)
auto_x_api = os.environ["AUTO_X_API"]
auto_x_url = os.environ["AUTO_X_URL"]
client = WebClient(token=os.environ["SLACK_TOKEN"])
channel_id = os.environ["CHANNEL_ID"]


def initial_message(response_url, headers, user):

    auto_x_article_initial_message = {
        "text": f"@{user} Please wait Auto-Extraction is Running"
    }
    auto_x_article_message_response = requests.post(
        url=response_url,
        headers=headers,
        data=json.dumps(auto_x_article_initial_message),
    )
    print(auto_x_article_message_response.status_code)
    return auto_x_article_message_response


def article(url, response_url, headers, user, slack_webhook_url):

    response = requests.post(
        f"{auto_x_url}",
        auth=(f"{auto_x_api}", ""),
        json=[{"url": f"{url}", "pageType": "article"}],
    )
    df = response.json()

    # print(df)

    if "error" in df[0]:

        print(df)
        auto_x_article_results = {
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"@{user} Auto-Extraction Article throwing error for {url} which is given below: \n\n {df}",
                    },
                }
            ]
        }
        auto_x_article_response = requests.post(
            url=response_url, headers=headers, data=json.dumps(auto_x_article_results),
        )
        print(auto_x_article_response.status_code)
        return auto_x_article_response

    else:

        # writing the response to the user.json file.
        f = open(f"{user}.json", "w")
        f.write(str(json.dumps(df)))
        f.close()

        auto_x_article_msg = {
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"@{user} Auto-Extraction Article results for {url} is given below: \n",
                    },
                }
            ]
        }
        auto_x_article_response = requests.post(
            url=slack_webhook_url, headers=headers, data=json.dumps(auto_x_article_msg),
        )
        print(auto_x_article_response.status_code)

        file_upload = client.files_upload(
            channels=f"{channel_id}",
            filetype="json",
            file=f"{user}.json",
            title=f"{url}",
            user=f"{user}",
        )
        print(file_upload.status_code)

        # gonna wait for 2 seconds after the upload and then delete the user.json to avoid space crunch on the server.
        time.sleep(2)
        os.remove(f"{user}.json")

        # The below part of the code is to post the resutls directly to the Response URL or USER (Visible Only) istead of a json file.

        # auto_x_article_results = {
        #     "text": f'Results: \n\n {df}'
        # }
        # auto_x_article_response = requests.post(
        #     url=response_url, headers=headers, data=json.dumps(auto_x_article_results))
        # print(auto_x_article_response.status_code)
        return auto_x_article_response


def article_list(url, response_url, headers, user, slack_webhook_url):

    response = requests.post(
        f"{auto_x_url}",
        auth=(f"{auto_x_api}", ""),
        json=[{"url": f"{url}", "pageType": "articleList"}],
    )
    df = response.json()

    # print(df)

    if "error" in df[0]:

        print(df)
        auto_x_article_results = {
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"@{user} Auto-Extraction Article throwing error for {url} which is given below: \n\n {df}",
                    },
                }
            ]
        }
        auto_x_article_response = requests.post(
            url=response_url, headers=headers, data=json.dumps(auto_x_article_results),
        )
        print(auto_x_article_response.status_code)
        return auto_x_article_response

    else:

        # writing the response to the user.json file.
        f = open(f"{user}.json", "w")
        f.write(str(json.dumps(df)))
        f.close()

        auto_x_article_msg = {
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"@{user} Auto-Extraction Article results for {url} is given below: \n",
                    },
                }
            ]
        }
        auto_x_article_response = requests.post(
            url=slack_webhook_url, headers=headers, data=json.dumps(auto_x_article_msg),
        )
        print(auto_x_article_response.status_code)

        file_upload = client.files_upload(
            channels=f"{channel_id}",
            filetype="json",
            file=f"{user}.json",
            title=f"{url}",
            user=f"{user}",
        )
        print(file_upload.status_code)

        # gonna wait for 2 seconds after the upload and then delete the user.json to avoid space crunch on the server.
        time.sleep(2)
        os.remove(f"{user}.json")

        # The below part of the code is to post the resutls directly to the Response URL or USER (Visible Only) istead of a json file.

        # auto_x_article_results = {
        #     "text": f'Results: \n\n {df}'
        # }
        # auto_x_article_response = requests.post(
        #     url=response_url, headers=headers, data=json.dumps(auto_x_article_results))
        # print(auto_x_article_response.status_code)
        return auto_x_article_response
