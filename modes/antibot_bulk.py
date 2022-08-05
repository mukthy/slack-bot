import requests
import validators
import pprint
import os
from pathlib import Path
from dotenv import load_dotenv
import json
import time

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

api = os.environ["APIKEY"]


def initial_message(user, slack_webhook_url, headers, response_url, urls):
    initial_scan_message = {
        "text": "Antibot Details",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"@{user} Starting the scan for {urls}. \n\n Please wait for the scan to complete. Go listen to a Song while you wait.",
                },
            },
        ],
    }

    resp = requests.post(
        url=response_url,
        headers=headers,
        data=json.dumps(initial_scan_message),
    )
    return resp


def check_url(urls):
    # urls = input("Enter the urls: ")

    # urls = ['https://www.truepeoplesearch.com/', 'zyte.com', 'https://allegro.pl/']

    urls = urls.split(', ')
    print(type(urls))

    valid_url = []
    invalid_url = []

    # print(validators.url(urls[0]))
    response = 'No Valid URLs'
    for url in urls:
        valid = validators.url(url)
        if valid:
            valid_url.append(url)
        else:
            invalid_url.append(url)

    print(f'this is a valid list {valid_url}')
    valid_resp = check_antibot(valid_url)
    pprint.pprint(response)

    invalid_resp = invalid_url_post(invalid_url)
    print(invalid_resp)
    print("Finally, Post the results to slack")
    return valid_resp, invalid_resp


def check_antibot(valid_url):
    anti_bots = []
    headers = {
        'accept': 'application/json',
        'apikey': f'{api}',
    }
    print(f'From with in the Check_Antibot fun {valid_url}')
    for url in valid_url:
        params = {
            'url': f'{url}',
            'apikey': f'{api}',
        }
        page_id = requests.get('https://antibotpedia.scrapinghub.com/api/check/add', headers=headers, params=params)
        page_id = json.loads(page_id.text)
        pprint.pprint(page_id)
        page = page_id["response"]["check_id"]
        print(f'Here is the AntiBot: https://antibotpedia.scrapinghub.com/checks/pages/{page}')
        page_url = f'https://antibotpedia.scrapinghub.com/checks/pages/{page}'

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
            time.sleep(10)

        final_result = json.loads(res.text)
        pprint.pprint(final_result)

        antibot_data = final_result["response"]["check"]["result"]["found"]
        app_matches = final_result["response"]["check"]["result"]["app_matches"]

        # antibot_data = json.dumps(antibot_data, indent=4)
        # app_matches = json.dumps(app_matches, indent=4)

        print(antibot_data)
        print(app_matches)

        anti_bots.append([antibot_data, app_matches, page_url])

    # creating a Dict with URL as key and the value is a list of antibot data and app matches
    result = {url: antibot for url, antibot in zip(valid_url, anti_bots)}

    result = json.dumps(result, indent=4)
    return result


def invalid_url_post(invalid_url=None):
    print(f'From with in the invalid_url_post fun {invalid_url}')
    return invalid_url


def post_results(user, headers, response_url, urls, valid, invalid):
    antibot_data = {
        "text": "Antibot Details",
        "blocks": [
            {
                "type": "section",
                "block_id": "section567",
                "text": {
                    "type": "mrkdwn",
                    "text": f"@{user} Antibot protection details for {urls} is below: \n\n :skull_and_crossbones: \n\n Valid URLs: {valid} \n\n Invalid URLs: {invalid}",
                },
            },
        ],
    }

    # print(antibot_data)

    # url = response_url  # this is the URL which was generated from the request that we did to scan the bot, it is a unique payload. If we use this we will be posting the data to the bot but it will be visible to the person who posted it.
    response = requests.post(
        url=response_url, headers=headers, data=json.dumps(
            antibot_data)
    )
    return response
