from typing import Union, Dict, Any
import requests
import json
import pprint
from datetime import date, datetime
from datetime import timedelta
import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(".") / ".env"
print(env_path)
load_dotenv(dotenv_path=env_path)
auth_key = os.environ['AUTH_KEY']
kibana_url = os.environ['KIBANA_URL']


def get_kibana_data(org_id, netloc, user, response_url, headers) -> Union[str, dict[str, Any]]:
    # Kibana API only gonna check for the last 24 hours.
    # Get the current date
    current_day: datetime = datetime.utcnow()
    current_day: date = current_day.date()

    today: str = current_day.strftime("%Y.%m.%d")
    print(today)

    # Subtract 1 day from the current date
    previous_day: date = current_day - timedelta(days=1)
    yesterday: str = previous_day.strftime("%Y.%m.%d")
    print(yesterday)

    # Apply that today and yesterday to the Kibana API date range.
    url = f"{kibana_url}{today},logstash-crawlera-requests-{yesterday}/_search"

    payload = json.dumps({
        "size": 0,
        "query": {
            "bool": {
                "should": [
                    {
                        "query_string": {
                            "query": "subtype:request"
                        }
                    }
                ]
            }
        },
        "aggs": {
            "filters": {
                "filter": {
                    "bool": {
                        "must": [
                            {
                                "term": {
                                    "netloc": f"{netloc}"
                                }
                            },
                            {
                                "query_string": {
                                    "query": f"organization_id:({org_id})"
                                }
                            }
                        ]
                    }
                },
                "aggs": {
                    "field": {
                        "terms": {
                            "field": "netloc",
                            "size": 10,
                            "order": {
                                "_count": "desc"
                            }
                        }
                    },
                    "missing": {
                        "missing": {
                            "field": "netloc"
                        }
                    }
                }
            }
        }
    })
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Basic {auth_key}',
        'Content-Type': 'application/json',
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:103.0) Gecko/20100101 Firefox/103.0'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    data = json.loads(response.text)
    pprint.pprint(data)

    if 'status' in data:
        print('No Data Found')
        return 'No Data Found'

    elif len(data['aggregations']['filters']['field']['buckets']) == 0:
        print('No Data Found')
        return 'No Data Found'

    else:
        domain = data['aggregations']['filters']['field']['buckets'][0]['key']
        count = data['aggregations']['filters']['field']['buckets'][0]['doc_count']

        requests_netloc_dict = {'Netloc': domain, 'Total Requests': count}
        requests_netloc_dict = json.dumps(requests_netloc_dict, indent=4)
        print(requests_netloc_dict)

        return requests_netloc_dict


def post_results(response_url, user, headers, results, netloc) -> str or dict[str, Any]:
    post_message = {
        "text": "Kibana Results",
        "blocks": [
            {
                "type": "section",
                "block_id": "section567",
                "text": {
                    "type": "mrkdwn",
                    "text": f"@{user} Kibana Data for {netloc} is given below:\n {results}"
                },
            },
        ],
    }

    response = requests.post(
        url=response_url, headers=headers, data=json.dumps(
            post_message)
    )
    return response
