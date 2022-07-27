import uncurl
import requests
import json
import os
import time
from dotenv import load_dotenv
from pathlib import Path
from slack_sdk import WebClient

env_path = Path(".", ".") / ".env"
load_dotenv(dotenv_path=env_path)
client = WebClient(token=os.environ["SLACK_TOKEN"])
channel_id = os.environ['CHANNEL_ID']


def initial_message(response_url, headers, user):
    curl_convertor_start = {
        "text": f"@{user}, Please wait while the Converter is Running \n"
    }
    curl_convertor_req = requests.post(
        url=response_url, headers=headers, data=json.dumps(
            curl_convertor_start)
    )
    print(curl_convertor_req.status_code)
    return curl_convertor_req


def convert(curl_input, user, slack_webhook_url, headers, response_url):
    # curl_input = input("Enter curl command: ")
    req_output = uncurl.parse(f"{curl_input}")

    with open(f"/home/mukthy/temp_files/{user}.py", "w") as f:
        f.write("import requests\n")
        f.write("response = ")
        f.write(req_output)
        f.write("\nprint(response.text)")

    curl_convertor_msg = {
        "text": "Curl Converter",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"@{user} Your CURL command to Python code is ready:\n ",
                },
            },
        ],
    }
    curl_convertor_response = requests.post(
        url=slack_webhook_url,
        headers=headers,
        data=json.dumps(curl_convertor_msg),
    )
    print(curl_convertor_response.status_code)

    file_upload = client.files_upload(
        channels=f"{channel_id}",
        filetype="python",
        file=f"/home/mukthy/temp_files/{user}.py",
        title=f"{user}",
        user=f"{user}",
    )
    print(file_upload.status_code)

    print(req_output)

    # gonna wait for 2 seconds after the upload and then delete the user.json to avoid space crunch on the server.
    time.sleep(2)
    os.remove(f"/home/mukthy/temp_files/{user}.py")
    print(f"{user}.py deleted")

    return req_output

# class Req:
#
#     def __init__(self, curl_input):
#         self.curl_input = curl_input
#
#     def curl_convertor(self):
#         req_output = uncurl.parse(self.curl_input)
#         with open("output.py", "w") as f:
#             f.write("import requests\n")
#             f.write("response = ")
#             f.write(req_output)
#             f.write("\nprint(response.text)")
#         return req_output
#
#
# curl_input = input("Enter curl command: ")
# r = Req(curl_input)
# print(r.curl_convertor())
# print("Done")

# curl_input = input("Enter curl command: ")
# req_output = uncurl.parse(f"{curl_input}")
#
# with open("output.py", "w") as f:
#     f.write("import requests\n")
#     f.write("response = ")
#     f.write(req_output)
#     f.write("\nprint(response.text)")
#
# print(req_output)
