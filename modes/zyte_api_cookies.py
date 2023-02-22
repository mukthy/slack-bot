import base64
import os
import time

import requests
import json
from dotenv import load_dotenv
from pathlib import Path
from slack_sdk import WebClient

headers = {"Content-Type": "application/json"}

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

zyte_api_key = os.environ["ZYTE_DATA_API"]
zyte_api_url = os.environ["ZYTE_DATA_API_URL"]
client = WebClient(token=os.environ["SLACK_TOKEN"])
channel_id = os.environ['CHANNEL_ID']

def http_response_cookies(url):
    payload = json.dumps(
        {
            "url": f"{url}",
            "httpResponseBody": True,
            "experimental": {
                "responseCookies": True,
            },
        }
    )

    response = requests.request(
        "POST",
        zyte_api_url,
        headers=headers,
        auth=(f"{zyte_api_key}", ""),
        data=payload,
    )
    print(response.text)
    cookies = response.json()["experimental"]["responseCookies"]
    return cookies


def http_request_cookies(url, cookies):
    payload = json.dumps(
        {
            "url": f"{url}",
            "httpResponseBody": True,
            "experimental": {
                "requestCookies": cookies,
            },
        }
    )

    response = requests.request(
        "POST",
        zyte_api_url,
        headers=headers,
        auth=(f"{zyte_api_key}", ""),
        data=payload,
    )
    # print(response.text)
    return response


def browser_html_request_cookies(url, cookies):
    payload = json.dumps(
        {
            "url": f"{url}",
            "browserHtml": True,
            "experimental": {
                "requestCookies": cookies,
            },
        }
    )

    response = requests.request(
        "POST",
        zyte_api_url,
        headers=headers,
        auth=(f"{zyte_api_key}", ""),
        data=payload,
    )
    # print(response.text)
    return response.text


def browser_html_response_cookies(url):
    payload = json.dumps(
        {
            "url": f"{url}",
            "browserHtml": True,
            "javascript": True,
            "actions": [
                {
                    "action": "waitForTimeout",
                    "timeout": 5,
                    "onError": "return"
                }
            ],
            "experimental": {
                "responseCookies": True,
            },
        }
    )

    response = requests.request(
        "POST",
        zyte_api_url,
        headers=headers,
        auth=(f"{zyte_api_key}", ""),
        data=payload,
    )
    # print(response.text)

    return response


def send_to_slack(response, user, slack_webhook_url, headers, url):
    f = open(f"{user}.html", "w")
    f.write(response)
    f.close()

    zyte_data_api_result = {
        "text": "Antibot Details",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"@{user} Zyte Data API results using Experimental Cookies for {url}:",
                },
            },
        ],
    }

    zyte_resp = requests.post(
        url=slack_webhook_url,
        headers=headers,
        data=json.dumps(zyte_data_api_result),
    )
    file_upload = client.files_upload(
        channels=f"{channel_id}",
        filetype="html",
        file=f"{user}.html",
        title=f"{url}",
        user=f"{user}",
    )
    print(file_upload.status_code)
    print(zyte_resp.status_code)
    time.sleep(2)
    os.remove(f"{user}.html")
    return zyte_resp


def send_errors_to_slack(zyte_api_error_result, user, slack_webhook_url, headers, url):

    zyte_data_api_result = {
        "text": "Antibot Details",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"@{user} Zyte Data API results for {url}:",
                },
            },
            {
                "type": "section",
                "block_id": "section567",
                "text": {
                    "type": "mrkdwn",
                    "text": f"Seems like ban or the length cookies exceeded! \n\n Use a different page url from {url} or Reach out to #smartbrowser-support team. \n\n The Result is given below: \n\n {zyte_api_error_result}",
                },
            },
        ],
    }
    zyte_resp = requests.post(
        url=slack_webhook_url,
        headers=headers,
        data=json.dumps(zyte_data_api_result),
    )
    return zyte_resp


def main(url, cookie_url, option, user, slack_webhook_url, headers):
    # url = "https://www.youtube.com/"
    # option = 'httpResponse'

    if option == 'httpResponse':
        browser_cookies_response = browser_html_response_cookies(url)
        if browser_cookies_response.status_code == 200:
            cookies = browser_cookies_response.json()["experimental"]["responseCookies"]
            print(cookies)
            if cookie_url == '':
                cookie_url = url
                print("URL is None, so taking default URL: ", cookie_url)
                response = http_request_cookies(cookie_url, cookies)
                print(response)
                return response

            else:
                print("URL is Given: ", cookie_url)
                response = http_request_cookies(cookie_url, cookies)
                if response.status_code == 200:
                    response = response.text
                    print(type(response))
                    with open('response.json', 'w') as f:
                        json.dump(response, f)
                    response = json.loads(response)
                    response = response["httpResponseBody"]
                    response = base64.b64decode(response)
                    response = response.decode("utf-8")
                    slack_response = send_to_slack(response, user, slack_webhook_url, headers, url)
                    print(slack_response)
                    return slack_response

                else:
                    print("Got cookies but error in getting response from Zyte API using HttpResponseBody")
                    slack_error_response = send_errors_to_slack(response.text, user, slack_webhook_url, headers, url)
                    print(slack_error_response)
                    return slack_error_response

        else:
            print("Error in getting cookies from Zyte API")
            slack_error_response = send_errors_to_slack(browser_cookies_response.text, user, slack_webhook_url, headers, url)
            print(slack_error_response)
            return slack_error_response

    # elif option == 'browserHtml':
    #     cookies = browser_html_response_cookies(url)
    #     print(cookies)
    #     url2 = input("Enter URL: ")
    #     print(url2)
    #     if url2 == '':
    #         url2 = url
    #         print("URL is None, so taking default URL: ", url2)
    #         response = browser_html_request_cookies(url2, cookies)
    #         print(response)
    #
    #     else:
    #         print("URL is Given: ", url2)
    #         response = browser_html_request_cookies(url2, cookies)
    #         print(response)


if __name__ == "__main__":
    main()
