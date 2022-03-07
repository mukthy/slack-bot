from slack_sdk import WebClient
import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, request, Response, render_template
import json
import requests
from time import sleep
import threading
import validators
import time

env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)

# client = slack.WebClient(token=os.environ['SLACK_TOKEN']) => For Old version of Slack-SDK
client = WebClient(token=os.environ['SLACK_TOKEN'])
api = os.environ['APIKEY']
# common webhook where the data will be posted to the bot directly and it will be visible to everyone.
slack_webhook_url = os.environ['SLACK_WEB_HOOK']
zyte_api = os.environ['ZYTE_DATA_API']
zyte_api_url = os.environ['ZYTE_DATA_API_URL']
spm_api = os.environ['SPM_API']
channel_id = os.environ['CHANNEL_ID']
headers = {
    'Content-type': 'application/json',
}


@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')


@app.route('/antibot', methods=['POST'])
def slack_response():
    data = request.form
    text = data.get('text')
    validators.url(text)
    user = data.get('user_name')
    response_url = data["response_url"]
    message = {
        "text": "Connection successful!"
    }
    resp = requests.post(response_url, json=message)
    print(resp.status_code)
    x = threading.Thread(
        target=antibot,
        args=(data, text, user, response_url)
    )
    x.start()
    return 'Processing, Please wait!!'


def antibot(data, text, user, response_url):

    # print(response_url)
    print(response_url)
    print(data)
    print(user)

    if validators.url(text) is True:

        initial_scan_message = {
            "text": 'Antibot Details',
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f'@{user} Please use the command: /antibot http://example.com'
                    }
                },
            ]
        }
        resp = requests.post(
            url=slack_webhook_url, headers=headers, data=json.dumps(initial_scan_message))

        print(resp.status_code)

        client.chat_postMessage(channel='#antibot-checker',
                                text='Sending request to Antibotpedia', response_type='in_channel')

        page_id = requests.get(
            f'https://antibotpedia.scrapinghub.com/api/check/add?url={text}&apikey={api}')

        print(page_id.text)
        dict1 = json.loads(page_id.text)
        page = dict1['response']['check_id']

        client.chat_postMessage(
            channel='#antibot-checker', text="Please wait. The scan takes atleast 1-2 mins time. Even on GUI", response_type='in_channel')
        client.chat_postMessage(
            channel='#antibot-checker', text=f"If you have access, you can check in the Web-UI: https://antibotpedia.scrapinghub.com/checks/pages/{page}", response_type='in_channel')

        res = requests.get(
            f'https://antibotpedia.scrapinghub.com/api/check/{page}?apikey={api}')
        print(res.text)
        dict2 = json.loads(res.text)
        finished = dict2['response']['check']['task']['finished']
        print(finished)
        # slack = json.loads(res.text)
        while finished is False:
            res = requests.get(
                f'https://antibotpedia.scrapinghub.com/api/check/{page}?apikey={api}')
            print(res.text)
            dict2 = json.loads(res.text)
            finished = dict2['response']['check']['task']['finished']
            sleep(20)

        final_result = res.json()
        print(final_result)
        antibot_data = final_result['response']['check']['result']['found']
        app_matches = final_result['response']['check']['result']['app_matches']

        antibot_data = {
            "text": 'Antibot Details',
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f'@{user} Results here: \n\n {antibot_data}'
                    }
                },
                {
                    "type": "section",
                    "block_id": "section567",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"@{user} Results for <https://{text}|{text}> is below: \n\n :skull_and_crossbones: \n\n {app_matches}"
                    },
                },
            ]
        }

        print(antibot_data)

        # url = response_url  # this is the URL which was generated from the request that we did to scan the bot, it is a unique payload. If we use this we will be posting the data to the bot but it will be visible to the person who posted it.
        response = requests.post(
            url=slack_webhook_url, headers=headers, data=json.dumps(antibot_data))

        print(response.status_code)
    else:

        incorrect_url_message = {
            "text": 'Antibot Details',
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f'@{user} Please enter a proper URL: https://example.com or http://example.com'
                    }
                },
            ]
        }
        resp = requests.post(
            url=response_url, headers=headers, data=json.dumps(incorrect_url_message))
        print(resp.status_code)

    return Response(), 200


@app.route('/help', methods=['POST'])
def slack_help():
    data = request.form
    user = data.get('user_name')
    # response_url = data["response_url"]
    help_message = {
        "text": 'Antibot Details',
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f'@{user} Please use the command: /antibot http://example.com'
                }
            },
        ]
    }
    resp = requests.post(
        url=slack_webhook_url, headers=headers, data=json.dumps(help_message))
    print(resp.status_code)

    return Response(), 200

# Region Checking Endpoint


@app.route('/regioncheck', methods=['POST'])
# the below function is to send a response as 200 to slack's post request within 3 sec to avoid the "operation_timed_out" error.
def slack_crawlbot_response():
    data = request.form
    text = data.get('text')
    validators.url(text)
    user = data.get('user_name')
    response_url = data["response_url"]
    message = {
        "text": "Connection successful!"
    }
    resp = requests.post(response_url, json=message)
    print(resp.status_code)
    crawl_bot = threading.Thread(
        target=crawlbot,
        args=(data, text, user, response_url)
    )
    crawl_bot.start()
    return 'Processing, Please wait!!'


def crawlbot(data, text, user, response_url):

    print(data)
    print(user)
    if validators.url(text) is True:
        regions = ['AU', 'AT', 'BY', 'BE', 'BO', 'BR', 'CA', 'CL', 'CN', 'DK', 'FI', 'FR', 'GE', 'DE', 'GR', 'HK', 'IN', 'ID', 'IE', 'IL', 'IT',
                   'JP', 'MY', 'MX', 'NL', 'NG', 'PH', 'PL', 'PT', 'RO', 'RU', 'SG', 'ZA', 'KR', 'ES', 'SE', 'CH', 'TW', 'TH', 'TR', 'AE', 'GB', 'US', 'UY']

        proxy_host = "proxy.crawlera.com"
        proxy_port = "8010"
        # Make sure to include ':' at the end
        proxy_auth = f"{spm_api}:"
        proxies = {
            "https": "http://{}@{}:{}/".format(proxy_auth, proxy_host, proxy_port),
            "http": "http://{}@{}:{}/".format(proxy_auth, proxy_host, proxy_port)
        }
        ok_result = []
        error_result = []
        threads = []
        starting_region_check = {
            "text": f"@{user} It may take upto 5 mins to complete, Go for a break or listen to a song :sweat_smile: "
        }
        requests.post(url=slack_webhook_url, json=starting_region_check)

        def send(text, headers, region):

            res = requests.get(url=f'{text}', headers=headers,
                               proxies=proxies, verify='/Users/mukthy/Desktop/office/slack_bots/slack-bot_dev/zyte-proxy-ca.crt')
            print(res.headers)
            if 'x-crawlera-slave' in res.headers:
                proxy_ip = res.headers['X-Crawlera-Slave']
                print(
                    f'The region {region} has a response of {res.status_code} status code from SPM. Proxy IP is {proxy_ip}')
                ok_result.append(
                    f'Country: {region} - Status: {res.status_code} - Proxy Details: {proxy_ip}')

            elif 'X-Crawlera-Error' in res.headers:
                proxy_ip = res.headers['X-Crawlera-Error']
                print(
                    f'The region {region} has a response of {res.status_code} status code from SPM. Proxy IP is {proxy_ip}')
                error_result.append(
                    f'Country: {region} - Status: {res.status_code} - Proxy Details: {proxy_ip}')

        def main():

            for region in regions:
                headers = {
                    'X-Crawlera-Region': f'{region}'
                }
                thread = threading.Thread(
                    target=send,
                    args=[text, headers, region]
                )
                thread.start()
                threads.append(thread)

            for thread in threads:
                thread.join()

            send(text, headers, region)

        main()
        print(ok_result)
        print(error_result)
        ok_result = json.dumps(ok_result)
        error_result = json.dumps(error_result)
        region_check_results = {
            "text": 'Antibot Details',
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f'@{user} Region-check results for {text}:'
                    }
                },
                {
                    "type": "section",
                    "block_id": "section567",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"200 OK Results: \n {ok_result} \n\n Results with Errors: \n {error_result}"
                    },
                },
            ]
        }
        resp = requests.post(
            url=slack_webhook_url, headers=headers, data=json.dumps(region_check_results))
        print(resp.status_code)

        # message = {
        #     "text": f"@{user} Proxy Region Check Result are below: \n\n {result} \n\n Do not Rely on this results alone. \n Adding specific headers, cookies and session may also help in avoiding 503."
        # }
        # resp = requests.post(url=slack_webhook_url, json=message)

        print(resp.status_code)
    else:
        incorrect_url_warning = {
            "text": 'Antibot Details',
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f'@{user} Please enter the proper URL like this http://{text} or https://{text} '
                    }
                },
            ]
        }
        resp = requests.post(
            url=response_url, headers=headers, data=json.dumps(incorrect_url_warning))
        print(resp.status_code)
    return Response(), 200


@app.route('/zytedataapi', methods=['POST'])
# the below function is to send a response as 200 to slack's post request within 3 sec to avoid the "operation_timed_out" error.
def slack_zyteapi_response():
    data = request.form
    text = data.get('text')
    validators.url(text)
    user = data.get('user_name')
    response_url = data["response_url"]
    message = {
        "text": "Connection successful!"
    }
    resp = requests.post(response_url, json=message)
    print(resp.status_code)
    zyte_api = threading.Thread(
        target=zytedataapi,
        args=(data, text, user, response_url)
    )
    zyte_api.start()
    return 'Processing, Please wait!!'


def zytedataapi(data, text, user, response_url):
    print(data)
    print(user)

    if validators.url(text) is True:
        starting_region_check = {
            "text": f"@{user} It may take upto 5 mins to complete, Go for a break or listen to a song :sweat_smile: "
        }
        requests.post(url=slack_webhook_url, json=starting_region_check)
        API_URL = f"{zyte_api_url}"
        API_KEY = f"{zyte_api}"
        response = requests.post(API_URL, auth=(API_KEY, ''), json={
            "url": f"{text}",
            "browserHtml": True,
            "javascript": True
        })
        zyte_api_result = response.json()
        if 'browserHtml' in zyte_api_result:

            print(zyte_api_result['browserHtml'])
            f = open(f'{user}.html', 'w')
            f.write(zyte_api_result['browserHtml'])
            f.close()
            zyte_data_api_result = {
                "text": 'Antibot Details',
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f'@{user} Zyte Data API results for {text}:'
                        }
                    },
                    # {
                    #     "type": "section",
                    #     "block_id": "section567",
                    #     "text": {
                    #         "type": "mrkdwn",
                    #         "text": f"The Result is given below: \n\n {final_result}"
                    #     },
                    # },
                ]
            }
            zyte_resp = requests.post(
                url=slack_webhook_url, headers=headers, data=json.dumps(zyte_data_api_result))
            file_upload = client.files_upload(
                channels=f'{channel_id}', filetype='html', file=f'{user}.html', title=f'{text}', user=f'{user}')
            print(file_upload.status_code)
            print(zyte_resp.status_code)
            time.sleep(2)
            os.remove(f'{user}.html')
        else:
            zyte_data_api_result = {
                "text": 'Antibot Details',
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f'@{user} Zyte Data API results for {text}:'
                        }
                    },
                    {
                        "type": "section",
                        "block_id": "section567",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"Seems like a Ban! \n\n Reach out to #uncork team. \n\n The Result is given below: \n\n {zyte_api_result}"
                        },
                    },
                ]
            }
            zyte_resp = requests.post(
                url=slack_webhook_url, headers=headers, data=json.dumps(zyte_data_api_result))

    else:
        incorrect_url_warning = {
            "text": 'Antibot Details',
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f'@{user} Please enter the proper URL like this http://{text} or https://{text} '
                    }
                },
            ]
        }
        zyte_resp = requests.post(
            url=response_url, headers=headers, data=json.dumps(incorrect_url_warning))
        print(zyte_resp.status_code)

    return Response(), 200


if __name__ == '__main__':
    app.run(port=5050, debug=True)
