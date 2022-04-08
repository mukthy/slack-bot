import requests
import json
from time import sleep


def get_page_id(url, api):
    headers = {
        "accept": "application/json",
        "apikey": f"{api}",
    }
    params = {
        "url": f"{url}",
        "apikey": f"{api}",
    }
    page_id = requests.get(
        "https://antibotpedia.scrapinghub.com/api/check/add",
        headers=headers,
        params=params,
    )
    return page_id


def initial_message(user, slack_webhook_url, headers):

    initial_scan_message = {
        "text": "Antibot Details",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"@{user} Please use the command: /antibot http://example.com",
                },
            },
        ],
    }

    resp = requests.post(
        url=slack_webhook_url, headers=headers, data=json.dumps(initial_scan_message),
    )
    return resp


def final_result(page, api):

    res = requests.get(
        f"https://antibotpedia.scrapinghub.com/api/check/{page}?apikey={api}"
    )
    print(res.text)
    dict2 = json.loads(res.text)
    finished = dict2["response"]["check"]["task"]["finished"]
    print(finished)
    # slack = json.loads(res.text)
    while finished is False:
        res = requests.get(
            f"https://antibotpedia.scrapinghub.com/api/check/{page}?apikey={api}"
        )
        print(res.text)
        dict2 = json.loads(res.text)
        finished = dict2["response"]["check"]["task"]["finished"]
        sleep(20)

    final_result = res.json()

    return final_result


def post_antibot_results(slack_webhook_url, headers, user, url, final_result):

    antibot_data = final_result["response"]["check"]["result"]["found"]
    app_matches = final_result["response"]["check"]["result"]["app_matches"]

    antibot_data = {
        "text": "Antibot Details",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"@{user} Results here: \n\n {antibot_data}",
                },
            },
            {
                "type": "section",
                "block_id": "section567",
                "text": {
                    "type": "mrkdwn",
                    "text": f"@{user} Results for <https://{url}|{url}> is below: \n\n :skull_and_crossbones: \n\n {app_matches}",
                },
            },
        ],
    }

    # print(antibot_data)

    # url = response_url  # this is the URL which was generated from the request that we did to scan the bot, it is a unique payload. If we use this we will be posting the data to the bot but it will be visible to the person who posted it.
    response = requests.post(
        url=slack_webhook_url, headers=headers, data=json.dumps(antibot_data)
    )
    return response
