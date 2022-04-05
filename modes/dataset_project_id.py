import requests
import json
import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(".", ".") / ".env"
load_dotenv(dotenv_path=env_path)
org_apikey = os.environ['ORG_API_KEY']


def initial_message(response_url, headers, user, dataset):
    dataset_project_start = {
        "text": f"@{user}, Please wait..! let me get the Project ID on which the DataSet {dataset} is Running \n"
    }
    dataset_project_response = requests.post(
        url=response_url, headers=headers, data=json.dumps(
            dataset_project_start)
    )
    print(dataset_project_response.status_code)
    return dataset_project_response


def get_dataset_project_id(org, dataset, user, response_url, headers):
    response = requests.get('https://app.scrapinghub.com/api/v2/organizations/' + org + '/autoextract/' + dataset,
                            auth=(org_apikey, ''))
    data = json.loads(response.text)
    spider = str(data.get('spider'))
    response = requests.get('https://app.scrapinghub.com/api/v2/spiders/' + spider, auth=(org_apikey, ''))
    data = json.loads(response.text)
    print(data)
    project = str(data.get('project').get('id'))
    sc_project_id = 'https://app.scrapinghub.com/p/' + project + '/jobs'
    #print(sc_project_id)
    dataset_project_msg = {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"@{user} Auto-Extraction's dataset {dataset} is running in the below given scrapy cloud "
                            f"project\n {sc_project_id} \n",
                },
            }
        ]
    }
    dataset_project_response = requests.post(
        url=response_url,
        headers=headers,
        data=json.dumps(dataset_project_msg),
    )
    print(dataset_project_response.status_code)
    return sc_project_id
