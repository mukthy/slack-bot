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


env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)

#client = slack.WebClient(token=os.environ['SLACK_TOKEN'])
client = WebClient(token=os.environ['SLACK_TOKEN'])
api = os.environ['APIKEY']
slack_webhook = os.environ['SLACK_WEB_HOOK']


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
        # if text is not None:

        client.chat_postMessage(channel='#antibot-checker',
                                text=f'@{user} has started the AntiBot Scan on {text}', response_type='in_channel')

        client.chat_postMessage(channel='#antibot-checker',
                                text='Sending request to Antibotpedia', response_type='in_channel')
        #print("Sending request to Antibotpedia")
        page_id = requests.get(
            f'https://antibotpedia.scrapinghub.com/api/check/add?url={text}&apikey={api}')

        print(page_id.text)
        dict1 = json.loads(page_id.text)
        page = dict1['response']['check_id']
        # client.chat_postMessage(channel='#antibot-checker',
        #                        text=f'this is the page id {page}', response_type='in_channel')

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

        headers = {
            'Content-type': 'application/json',
        }
        #print(f"Antibots Found {antibot_data}")
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
        # common webhook where the data will be posted to the bot directly and it will be visible to everyone.
        url = f'{slack_webhook}'
        # url = response_url  # this is the URL which was generated from the request that we did to scan the bot, it is a unique payload. If we use this we will be posting the data to the bot but it will be visible to the person who posted it.
        response = requests.post(
            url, headers=headers, data=json.dumps(antibot_data))

        print(response.status_code)
    else:
        client.chat_postMessage(
            channel='#antibot-checker', text="Please enter a proper URL", response_type='in_channel')

    return Response(), 200


@app.route('/help', methods=['POST'])
def slack_help():
    #data = request.form
    #response_url = data["response_url"]
    message = {
        "text": "Please use the command: /antibot http://example.com"
    }
    resp = requests.post(
        url=f'{slack_webhook}', json=message)
    print(resp.status_code)

    return Response(), 200
    # client.chat_postMessage(channel='#antibot-checker',
    #                        text="Please use the given command: /antibot example.com", response_type='in_channel')


#ray.get(ray.slack_response(), ray.message_count())
if __name__ == '__main__':
    app.run(debug=True)
