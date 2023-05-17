import json
import os
import sys
import time

import requests


def run(url, response_url, headers, user):
    # url = sys.argv[1]
    print(url)
    a = os.popen(
        f'cd /home/mukthy/Desktop/slack-bot_dev/modes/DFPM && xvfb-run --server-args="-screen 0 1024x768x24" --auto-servernum node dfpm.js --runChrome google-chrome {url} --webhook http://127.0.0.1:8001/webhook --exit {url}').read()
    print(a)
    pid =
    if 'Exiting because of --exit flag' in a:
        print('Matched')
        print('DFPM Completed')
        # exit()
        # with open("/home/mukthy/Desktop/slack-bot_dev/modes/DFPM/final_data.json", "r") as f:
        #     fingerprint = f.read()
        # # os.remove("/home/mukthy/Desktop/slack-bot_dev/modes/DFPM/final_data.json")
        fingerprint = open("/home/mukthy/Desktop/slack-bot_dev/modes/DFPM/final_data.json", "r")
        bf = json.load(fingerprint)
        print(bf)

        if len(bf["fingerprint"]) > 1:
            print(bf)
            # fingerprint = bf["fingerprint"]
            # bf = {
            #     "browser_fingerprint": fingerprint,
            # }
            # with open("bf.json", "w") as outfile:
            #     json.dump(bf, outfile, indent=4)

            bf = json.dumps(bf, indent=4)
            print(bf)
            bf_data = {
                "text": "Antibot Details",
                "blocks": [
                    {
                        "type": "section",
                        "block_id": "section567",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"@{user} Browser Fingerprinting for <https://{url}|{url}> is below: \n\n :alert: \n\n {bf}",
                        },
                    },
                ],
            }

            # print(antibot_data)

            # url = response_url  # this is the URL which was generated from the request that we did to scan the bot, it is a unique payload. If we use this we will be posting the data to the bot but it will be visible to the person who posted it.
            response = requests.post(
                url=response_url, headers=headers, data=json.dumps(
                    bf_data, indent=4)
            )
            print(response)
            return response.text

        else:
            bf_data = {
                "text": "Antibot Details",
                "blocks": [
                    {
                        "type": "section",
                        "block_id": "section567",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"@{user} No Browser Fingerprinting Found for <https://{url}|{url}>, You can try manually.",
                        },
                    },
                ],
            }

            # print(antibot_data)

            # url = response_url  # this is the URL which was generated from the request that we did to scan the bot, it is a unique payload. If we use this we will be posting the data to the bot but it will be visible to the person who posted it.
            response = requests.post(
                url=response_url, headers=headers, data=json.dumps(
                    bf_data, indent=4)
            )
            print(response)
            return response.text

        os.remove("/home/mukthy/Desktop/slack-bot_dev/modes/DFPM/final_data.json")

    elif 'dfpm running...' in a or 'chrome has closed' in a:
        print('Matched')
        print('DFPM already running')
        time.sleep(45)
        run(url, response_url, headers, user)


if __name__ == '__main__':
    run(url, response_url, headers, user)
