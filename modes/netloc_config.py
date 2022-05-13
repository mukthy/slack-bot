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
    # print(query_url)

    payload = {}

    header = {"Content-Type": "application/json"}

    response = requests.request(
        "GET", url=query_url, auth=(django_user_api, ""), headers=headers, data=payload
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

        def datas(url):
            data = netloc_api_result["results"][0:]
            # pprint.pprint(data[0])
            # print(len(data))
            # print(len(data[0]))
            # print(data[0]['organization_name'])
            num = int(len(data))
            for n in range(num):
                dict1 = data[n]
                if "organization_name" not in dict1 and f"{url}".lower() == dict1["netloc_name"]:
                    # print(dict1['organization_name'])
                    # pprint.pprint(dict1)

                    # Spliting the BanRules and Other Configs of CCM separately because the JSON Post data to slack returns 400 Bad request.
                    # dict2 = json.dumps(dict1, indent=4)
                    banrules = dict1["ban_rules"]
                    banrules_final = json.dumps(banrules, indent=4)
                    # print(banrules_final)

                    # The below part is for Other Configs (GL, SPW, Initial Jail Time etc) of CCM separately because the JSON Post data to slack returns 400 Bad request.
                    rest_dict = {
                        key: val for key, val in dict1.items() if key != "ban_rules"
                    }
                    rest_dict_final = json.dumps(rest_dict, indent=4)
                    print(rest_dict_final)

                    # If we want to store the JSON in a file and post it in the #channel then un-comment from line 87 to 90 and uncomment from line 126 to 162
                    # f = open(f"{user}.json", "w")
                    # f.write(str(dict1))
                    # f.close()
                    # print("File Written")

                    netloc_config_results = {
                        "text": "Antibot Details",
                        "blocks": [
                            {
                                "type": "section",
                                "text": {
                                    "type": "mrkdwn",
                                    "text": f"@{user} Netloc-Config for {url} is below:\n {banrules_final}",
                                },
                            },
                            {
                                "type": "section",
                                "text": {
                                    "type": "mrkdwn",
                                    "text": f"{rest_dict_final}",
                                },
                            },
                        ],
                    }
                    netloc_config_resps = requests.post(
                        url=slack_webhook_url,
                        headers=header,
                        data=json.dumps(netloc_config_results),
                    )

                    # Leaving the below snippet as it was created due to the JSON post data to Slack was returning with 400 Bad Request.
                    # rest_dict_final_results = {
                    #     "text": "Antibot Details",
                    #     "blocks": [
                    #         {
                    #             "type": "section",
                    #             "text": {
                    #                 "type": "mrkdwn",
                    #                 "text": f"{rest_dict_final}",
                    #             },
                    #         },
                    #     ],
                    # }
                    # rest_dict_final_resps = requests.post(
                    #     url=response_url,
                    #     headers=header,
                    #     data=json.dumps(rest_dict_final_results),
                    # )
                    # print(rest_dict_final_resps)

                    # file_upload = client.files_upload(
                    #     channels=f"{channel_id}",
                    #     filetype="json",
                    #     file=f"{user}.json",
                    #     title=f"{url}",
                    #     user=f"{user}",
                    # )
                    # print(file_upload.status_code)
                    # print(netloc_resps.status_code)
                    # time.sleep(2)
                    # os.remove(f"{user}.json")
                    print(netloc_config_resps)
                    return netloc_config_resps
            else:
                print("Config does not exists")
                netloc_config_result = {
                    "text": "Antibot Details",
                    "blocks": [
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": f"@{user} Netloc Config not present for {url}.\n Try with a Full Domain for ex: domain.com!",
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

        datas(url)
