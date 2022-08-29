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

    full_result: list = []

    today: str = current_day.strftime("%Y.%m.%d")
    print(today)

    # Subtract 1 day from the current date
    previous_day: date = current_day - timedelta(days=1)
    yesterday: str = previous_day.strftime("%Y.%m.%d")
    print(yesterday)

    # Apply that today and yesterday to the Kibana API date range.
    url = f"{kibana_url}{today},logstash-crawlera-requests-{yesterday}/_search"

    # Payload to check the total number of request sent to a netloc from Kibana else return No Data.

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
        full_result.append('No Data Found')

    elif len(data['aggregations']['filters']['field']['buckets']) == 0:
        print('No Data Found')
        full_result.append('No Data Found')

    else:
        domain = data['aggregations']['filters']['field']['buckets'][0]['key']
        count = data['aggregations']['filters']['field']['buckets'][0]['doc_count']

        requests_netloc_dict = {'Netloc': domain, 'Total Requests': count}
        requests_netloc_dict = json.dumps(requests_netloc_dict, indent=4)
        full_result.append(requests_netloc_dict)

# Payload to check the error status codes from Kibana else return No Data.
    errors_payload = json.dumps({
        "size": 0,
        "query": {
            "bool": {
                "should": [
                    {
                        "query_string": {
                            "query": "subtype:request AND _exists_:error_details"
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
                            "field": "code",
                            "size": 10,
                            "order": {
                                "_count": "desc"
                            }
                        }
                    },
                    "missing": {
                        "missing": {
                            "field": "code"
                        }
                    }
                }
            }
        }
    })

    errors_total_requests = requests.request("POST", url, headers=headers, data=errors_payload)
    errors_total_data = json.loads(errors_total_requests.text)
    # pprint.pprint(errors_total_data)

    if 'status' in errors_total_data:
        print('No Data Found')
        full_result.append('No Data Found in Error Status Codes')
        # return full_result

    elif len(errors_total_data['aggregations']['filters']['field']['buckets']) == 0:
        print('No Data Found')
        full_result.append('No Data Found in Error Status Codes')
        # return full_result

    else:
        error_counts = len(errors_total_data['aggregations']['filters']['field']['buckets'])
        for error_count in range(error_counts):
            error_code = errors_total_data['aggregations']['filters']['field']['buckets'][error_count]['key']
            error_count = errors_total_data['aggregations']['filters']['field']['buckets'][error_count]['doc_count']

            errors_netloc_dict = {'errors': error_code, 'total_count': error_count}
            # print(errors_netloc_dict)
            full_result.append(errors_netloc_dict)

    # pprint.pprint(full_result)

# Payload to check the error details from Kibana else return No Data.
    errors_details_payload = json.dumps({
        "size": 0,
        "query": {
            "bool": {
                "should": [
                    {
                        "query_string": {
                            "query": "subtype:*"
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
                            "field": "error_details.raw",
                            "size": 10,
                            "order": {
                                "_count": "desc"
                            }
                        }
                    },
                    "missing": {
                        "missing": {
                            "field": "error_details.raw"
                        }
                    }
                }
            }
        }
    })

    errors_details_requests = requests.request("POST", url, headers=headers, data=errors_details_payload)
    errors_details_total_data = json.loads(errors_details_requests.text)
    pprint.pprint(errors_details_total_data)

    if 'status' in errors_details_total_data:
        print('No Data Found')
        full_result.append('No Data Found in Error Details')
        # return full_result

    elif len(errors_details_total_data['aggregations']['filters']['field']['buckets']) == 0:
        print('No Data Found')
        full_result.append('No Data Found in Error Details')
        # return full_result

    else:
        error_details_counts = len(errors_details_total_data['aggregations']['filters']['field']['buckets'])
        print(error_details_counts)
        for error_details_count in range(error_details_counts):
            error_details = \
                errors_details_total_data['aggregations']['filters']['field']['buckets'][error_details_count]['key']
            total_count = \
                errors_details_total_data['aggregations']['filters']['field']['buckets'][error_details_count][
                    'doc_count']

            errors_netloc_dict = {'errors_detail': error_details, 'total_count': total_count}
            # print(errors_netloc_dict)
            full_result.append(errors_netloc_dict)

    full_result = json.dumps(full_result, indent=4)
    print("Full Results Below:")
    print(full_result)
    return full_result


def post_results(response_url, user, headers, results, netloc, temp_url) -> str or dict[str, Any]:
    post_message = {
        "text": "Kibana Results",
        "blocks": [
            {
                "type": "section",
                "block_id": "section567",
                "text": {
                    "type": "mrkdwn",
                    "text": f"@{user} You can also use Kibana Temp URL:\n {temp_url}\n\n Kibana Data for {netloc} is given below:\n {results}"
                },
            },
        ],
    }

    response = requests.post(
        url=response_url, headers=headers, data=json.dumps(
            post_message)
    )
    return response
