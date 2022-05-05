import json
import requests
import time
import pprint
from slack import WebClient
from slack_sdk import WebClient
import os
from dotenv import load_dotenv
from pathlib import Path


def initial_message(response_url, user):
    initial_msg = {
        "text": f"@{user} Give me a min Fetching results :sweat_smile: "
    }
    initial_response = requests.post(
        url=response_url, json=initial_msg)
    return initial_response


env_path = Path(".") / ".env"
print(env_path)
load_dotenv(dotenv_path=env_path)
django_user_api = os.environ["DJANGO_USER_API"]
api_url = os.environ["NETLOC_API_URL"]
client = WebClient(token=os.environ["SLACK_TOKEN"])
channel_id = os.environ['CHANNEL_ID']


def default_netloc_config(url, user, slack_webhook_url, headers, response_url):

    query_url = f"{api_url}{url}"
    payload = {}
    # print(query_url)

    payload = {}

    response = requests.request(
        "GET", url=url, auth=(django_user_api, ""), headers=headers, data=payload
    )

    #
    netloc_api_result = json.loads(response.text)

    print(netloc_api_result["count"])
    if netloc_api_result["count"] == 0:
        print(f"No Netloc Config for {url}, You should Create One!")
        netloc_config_result = {
            "text": "Antibot Details",
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"@{user} No Default/Global-Netloc Config for {url}, You should Create One!",
                    },
                },
            ],
        }
        netloc_resp = requests.post(
            url=response_url,
            headers=headers,
            data=json.dumps(netloc_config_result),
        )
        return netloc_resp

    else:
        # print(res['count'])
        # page2 = res['next']

        def datas(res, netloc):
            data = res["results"][0:]
            # pprint.pprint(data[0])
            # print(len(data))
            # print(len(data[0]))
            # print(data[0]['organization_name'])
            num = int(len(data))
            for n in range(num):
                # if 'Data on Demand' not in data[n]['organization_name']:
                #     print(data[n]['organization_name'])
                #     break
                # elif 'Data on Demand' in data[n]['organization_name']:
                #     pprint.pprint(data[n]['netloc_name'])
                # print(n)
                # pprint.pprint(data[n])
                dict1 = data[n]
                if "organization_name" not in dict1 and dict1["netloc_name"] == f"{netloc}":
                    # print(dict1['organization_name'])
                    # pprint.pprint(dict1)
                    dict2 = json.dumps(dict1, indent=4)
                    # If we want to store the JSON in a file and post it in the #channel then un-comment from line 87 to 90 and uncomment from line 126 to 162
                    # f = open(f"{user}.json", "w")
                    # f.write(str(dict1))
                    # f.close()
                    # print("File Written")
                else:
                    print("Config does not exists")


        datas(netloc_api_result, url)
        while netloc_api_result["next"] is not None:
            next_page = netloc_api_result["next"]
            # print(f"this is line 68 {next_page}")
            response = requests.request(
                "GET",
                url=next_page,
                auth=(django_user_api, ""),
                headers=headers,
                data=payload,
            )
            # print(response.text)
            netloc_api_result = json.loads(response.text)
            next_page = netloc_api_result["next"]
            print(next_page)
            datas(netloc_api_result, url)
        # else res['next'] is None:
        #     print('Next Page Does not Exist')

        # This below part of the code is used to upload a file with the Json result and delete it once it is uploaded to slack
        # netloc_config_result = {
        #     "text": "Antibot Details",
        #     "blocks": [
        #         {
        #             "type": "section",
        #             "text": {
        #                 "type": "mrkdwn",
        #                 "text": f"@{user} Netloc Config results for {url}:",
        #             },
        #         },
        #         # {
        #         #     "type": "section",
        #         #     "block_id": "section567",
        #         #     "text": {
        #         #         "type": "mrkdwn",
        #         #         "text": f"The Result is given below: \n\n {final_result}"
        #         #     },
        #         # },
        #     ],
        # }
        # netloc_resp = requests.post(
        #     url=slack_webhook_url,
        #     headers=headers,
        #     data=json.dumps(netloc_config_result),
        # )
        # file_upload = client.files_upload(
        #     channels=f"{channel_id}",
        #     filetype="json",
        #     file=f"{user}.json",
        #     title=f"{url}",
        #     user=f"{user}",
        # )
        # print(file_upload.status_code)
        # print(netloc_resp.status_code)
        # time.sleep(2)
        # os.remove(f"{user}.json")
        # return netloc_resp
