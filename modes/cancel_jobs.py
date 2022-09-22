import time

import requests
import json


def main_start(project_id, spider_id, api_key) -> str:

    def start():

        url = f"https://jobq.scrapinghub.com/jobq/{project_id}/{spider_id}/cancel?&apikey={api_key}"

        payload = {}
        job_headers = {}

        response = requests.request("POST", url, headers=job_headers, data=payload)

        data = json.loads(response.text)

        print(data)
        count = data['count']
        while count > 0:
            time.sleep(5)
            start()
            break

    start()
    return 'All jobs cancelled'


def post_results(user, headers, response_url, cancel_jobs_results, project_id, spider_id) -> requests.Response:
    post_message = {
        "text": "Bulk Scrapy Cloud Job Cancel Results",
        "blocks": [
            {
                "type": "section",
                "block_id": "section567",
                "text": {
                    "type": "mrkdwn",
                    "text": f"@{user}:\n{cancel_jobs_results} for project {project_id} and spider {spider_id}\n Please check: https://app.zyte.com/p/{project_id}/jobs"
                },
            },
        ],
    }

    response = requests.post(
        url=response_url, headers=headers, data=json.dumps(
            post_message)
    )
    return response


def incorrect_format(response_url, headers, user) -> requests.Response:
    payload = {
        "text": "Intercepted Requests",
        "blocks": [
            {
                "type": "section",
                "block_id": "section567",
                "text": {
                    "type": "mrkdwn",
                    "text": f"@{user} Please enter the correct format:\n `/zytebot-cancel-jobs <project_id>, <spider_id>, <api_key>`\n `/zytebot-cancel-jobs 564968, 1, bb31dd1bf40e4c7a8838547e372af86c`\n"
                },
            },
        ],
    }

    response = requests.post(url=response_url, headers=headers, data=json.dumps(payload))
    return response
