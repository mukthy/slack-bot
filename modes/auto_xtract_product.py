import requests
import json
import os
from dotenv import load_dotenv
from pathlib import Path
import time
from slack_sdk import WebClient

env_path = Path(".", ".") / ".env"
load_dotenv(dotenv_path=env_path)
auto_x_api = os.environ['AUTO_X_API']
auto_x_url = os.environ['AUTO_X_URL']
client = WebClient(token=os.environ["SLACK_TOKEN"])
channel_id = os.environ['CHANNEL_ID']


def initial_message(response_url, headers, user):
    auto_x_product_start = {
        "text": f"@{user}, Please wait Auto-Extraction is Running \n"
    }
    auto_x_product_response = requests.post(
        url=response_url, headers=headers, data=json.dumps(
            auto_x_product_start)
    )
    print(auto_x_product_response.status_code)
    return auto_x_product_response


def product(url, response_url, headers, user, slack_webhook_url):

    product_response = requests.post(
        f"{auto_x_url}",
        auth=(f"{auto_x_api}", ""),
        json=[{"url": f"{url}", "pageType": "product"}],
    )
    df = product_response.json()

    # print(df)

    if "error" in df[0]:

        print(df)
        auto_x_product_list_results = {
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"@{user} Auto-Extraction Product throwing error for {url} which is given below: \n\n {df}",
                    },
                }
            ]
        }
        auto_x_product_list_response = requests.post(
            url=response_url,
            headers=headers,
            data=json.dumps(auto_x_product_list_results),
        )
        print(auto_x_product_list_response.status_code)
        return auto_x_product_list_response

    else:

        # writing the response to the user.json file.
        f = open(f"{user}.json", "w")
        f.write(str(json.dumps(df)))
        f.close()

        auto_x_product_msg = {
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"@{user} Auto-Extraction Product results for {url} is given below: \n",
                    },
                }
            ]
        }
        auto_x_product_response = requests.post(
            url=slack_webhook_url,
            headers=headers,
            data=json.dumps(auto_x_product_msg),
        )
        print(auto_x_product_response.status_code)

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

        # auto_x_product_results = {
        #     "text": f'Results: \n\n {df}'
        # }
        # auto_x_product_results = requests.post(
        #     url=response_url, headers=headers, data=json.dumps(auto_x_product_results))
        # print(auto_x_product_results.status_code)


def product_list(url, response_url, headers, user, slack_webhook_url):

    product_list_response = requests.post(
        f"{auto_x_url}",
        auth=(f"{auto_x_api}", ""),
        json=[{"url": f"{url}", "pageType": "productList"}],
    )
    df = product_list_response.json()

    # print(df)
    if "error" in df[0]:

        print(df)
        auto_x_product_list_results = {
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"@{user} Auto-Extraction Product List throwing error for {url} which is given below: \n\n {df}",
                    },
                }
            ]
        }
        auto_x_product_list_response = requests.post(
            url=response_url,
            headers=headers,
            data=json.dumps(auto_x_product_list_results),
        )
        print(auto_x_product_list_response.status_code)

    else:
        # writing the response to the user.json file.
        f = open(f"{user}.json", "w")
        f.write(str(json.dumps(df)))
        f.close()

        auto_x_product_list_msg = {
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"@{user} Auto-Extraction Product Listing results for {url} is given below: \n",
                    },
                }
            ]
        }
        auto_x_product_list_response = requests.post(
            url=slack_webhook_url,
            headers=headers,
            data=json.dumps(auto_x_product_list_msg),
        )
        print(auto_x_product_list_response.status_code)

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

        # auto_x_product_list_results = {
        #     "text": f'Results: \n\n {df}'
        # }
        # auto_x_product_list_response = requests.post(
        #     url=response_url, headers=headers, data=json.dumps(auto_x_product_list_results))
        # print(auto_x_product_list_response.status_code)
