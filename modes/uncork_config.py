import pprint
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
        "text": f"@{user} Give me a min Fetching results :sweat_smile: "
    }
    initial_response = requests.post(
        url=response_url, json=initial_msg)
    return initial_response


env_path = Path(".", ".") / ".env"
print(env_path)
load_dotenv(dotenv_path=env_path)
django_user_api = os.environ['DJANGO_USER_API']
api_url = os.environ['UNCORK_API_URL']
client = WebClient(token=os.environ["SLACK_TOKEN"])


def default_uncork_config(url, user, slack_webhook_url, headers, response_url):
    query_url = f"{api_url}{url}"
    payload = {}
    response = requests.request("GET",
                                query_url,
                                auth=(django_user_api, ""),
                                data=payload,
                                )
    uncork_api_result = json.loads(response.text)
    print(uncork_api_result['count'])

    if uncork_api_result['count'] == 0:

        print(uncork_api_result['count'])
        print(f'No Netloc Config for {url}, You should Create One!')
        uncork_config_result = {
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
        uncork_resp = requests.post(
            url=response_url,
            headers=headers,
            data=json.dumps(uncork_config_result),
        )
        return uncork_resp

    else:

        def datas(uncork_api_result, url):
            data = uncork_api_result['results'][0:]
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
                # if "organization_name" not in dict1 and dict1['netloc_name'] == f'{url}':
                if dict1['netloc_name'] == f'{url}'.lower():
                    # print(dict1['organization_name'])
                    # pprint.pprint(dict1)
                    dict2 = json.dumps(dict1, indent=4)
                    print(dict2)
                    # If we want to store the JSON in a file and post it in the #channel then un-comment from line 87 to 90 and uncomment from line 126 to 162
                    # f = open(f"{user}.json", "w")
                    # f.write(str(dict2))
                    # f.close()
                    # print('File Written')
                    netloc_config_results = {
                        "text": "Antibot Details",
                        "blocks": [
                            {
                                "type": "section",
                                "text": {
                                    "type": "mrkdwn",
                                    "text": f"@{user} Default Netloc-Config Results:\n {dict2}",
                                },
                            },
                        ],
                    }
                    uncork_resps = requests.post(
                        url=response_url,
                        headers=headers,
                        data=json.dumps(netloc_config_results),
                    )
                    return uncork_resps
                else:
                    print("Config does not exists")
                    uncork_config_result = {
                        "text": "Antibot Details",
                        "blocks": [
                            {
                                "type": "section",
                                "text": {
                                    "type": "mrkdwn",
                                    "text": f"@{user} Uncork-Config not found for {url}.\n Please try with full domain for ex: domain.com!",
                                },
                            },
                        ],
                    }
                    uncork_resp = requests.post(
                        url=response_url,
                        headers=headers,
                        data=json.dumps(uncork_config_result),
                    )
                    return uncork_resp

        datas(uncork_api_result, url)
        while uncork_api_result['next'] is not None:
            next_page = uncork_api_result['next']
            # print(next_page)
            response = requests.request("GET", url=next_page, auth=(django_user_api, ""), headers=headers, data=payload)
            # print(response.text)
            uncork_api_result = json.loads(response.text)
            next_page = uncork_api_result['next']
            print(next_page)
            datas(uncork_api_result, url)

        # else res['next'] is None:
        #     print('Next Page Does not Exist')

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
        #     channels="C02NY5ME01L",
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
