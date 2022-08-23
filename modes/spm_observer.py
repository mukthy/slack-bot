import asyncio
import time
import websockets
import json
import pprint
import base64
import os
from dotenv import load_dotenv
from pathlib import Path
import requests
from bs4 import BeautifulSoup
from slack_sdk import WebClient

env_path = Path(".") / ".env"
print(env_path)
load_dotenv(dotenv_path=env_path)
partial_socket_url = os.environ['PARTIAL_SOCKET_URL']
auth_key = os.environ['AUTH_KEY']
observer_url = os.environ['OBSERVER_URL']
client = WebClient(token=os.environ["SLACK_TOKEN"])
channel_id = os.environ['CHANNEL_ID']


def initial_message(user, slack_webhook_url, headers, response_url):
    initial_scan_message = {
        "text": "Starting Scan",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"@{user} Checking if entered parameters are valid..."
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


def get_auth_key() -> str:
    url = f"{observer_url}"

    payload = {}
    headers = {
        'Authorization': f'Basic {auth_key}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    soup = BeautifulSoup(response.text, 'html.parser')
    all_scripts = soup.find_all('script')
    user_token = all_scripts[0].text.split(' ')[3].replace('"', '')
    print(f"User token: {user_token}")
    return user_token


# get_aut_key()
def spm_interceptor(org_id, crawlera_node, count, user, response_url, headers):
    async def interceptor() -> list[str]:

        user_token = get_auth_key()

        message = f'{{"log_body":false,"log_bytes":1024,"event_number":{count},"crawlera_master":"{crawlera_node}","expression":"org_id == {org_id}"}}'
        print(message)

        message_bytes = message.encode('ascii')
        base64_bytes = base64.b64encode(message_bytes)
        base64_query_message = base64_bytes.decode('ascii')
        print(base64_query_message)

        null_message = {}
        send_message = f'["1","1","tracer:{base64_query_message}","phx_join",{null_message}]'
        print(send_message)

        socket_url = f'{partial_socket_url}{user_token}&vsn=2.0.0'
        print(f"Socket URL: {socket_url}")

        async with websockets.connect(f'{socket_url}') as websocket:
            await websocket.send(
                f'{send_message}')
            res = await websocket.recv()
            # print(res)
            res = json.loads(res)
            print(res)
            check = res[4]
            print(check)

            if check['status'] == 'error':
                return check

            else:

                full_result = []

                for i in range(count):
                    data1 = f'''
                    Intercepted Request {i}:
                    ====================
                    '''
                    data2 = '''
                    ====================
                    '''

                    intercepted = await websocket.recv()
                    intercepted = json.loads(intercepted)
                    pprint.pprint(intercepted[4])
                    stripped_data = (str(json.dumps(intercepted[4], indent=4))).replace('\\', '').replace('""', '"')

                    full_result.append(stripped_data)

                    with open(f'{user}.json', 'a') as f:
                        f.write(f'{data1}\n')
                        f.write(f'{stripped_data}\n')
                        f.write(f'\n{data2}')
                        f.close()

            print(full_result)
            return check

    return asyncio.run(interceptor())


def post_results(user, headers, slack_webhook_url, org_id, crawlera_node):
    intercepted_messsage = {
        "text": "Intercepted Requests",
        "blocks": [
            {
                "type": "section",
                "block_id": "section567",
                "text": {
                    "type": "mrkdwn",
                    "text": f"@{user} Intercepted Requests of Org_ID: {org_id} & Node: {crawlera_node} are stored in the file attached below:\n"
                },
            },
        ],
    }

    response = requests.post(
        url=slack_webhook_url, headers=headers, data=json.dumps(
            intercepted_messsage)
    )
    file_upload = client.files_upload(
        channels=f"{channel_id}",
        filetype="json",
        file=f"{user}.json",
        title="Intercepted Requests",
        user=f"{user}",
    )
    print(file_upload.status_code)
    time.sleep(2)
    os.remove(f"{user}.json")
    return response


def incorrect_format(response_url, user, headers):
    incorrect_format_messsage = {
        "text": "Intercepted Requests",
        "blocks": [
            {
                "type": "section",
                "block_id": "section567",
                "text": {
                    "type": "mrkdwn",
                    "text": f"@{user} Incorrect format, please enter as follows: \n `/zyte-bot-spm-observer 382142, cm-31-sep020, 10`"
                },
            },
        ],
    }

    response = requests.post(
        url=response_url, headers=headers, data=json.dumps(
            incorrect_format_messsage)
    )
    return response


def error_message(user, response_url, headers, result):
    error_msg = {
        "text": "Intercepted Requests",
        "blocks": [
            {
                "type": "section",
                "block_id": "section567",
                "text": {
                    "type": "mrkdwn",
                    "text": f"@{user} Encounter an Error, please check:\n {result}"
                },
            },
        ],
    }

    error_message_response = requests.post(
        url=response_url, headers=headers, data=json.dumps(
            error_msg)
    )
    return error_message_response
