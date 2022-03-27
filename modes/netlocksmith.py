import requests
import json
import os
from dotenv import load_dotenv
from pathlib import Path
import pandas as pd

env_path = Path(".", ".") / ".env"
load_dotenv(dotenv_path=env_path)
netloc_api = os.environ['NETLOC_API']
netloc_url = os.environ['NETLOC_URL']


def netloc(url, user, response_url, headers):
    post_data = json.dumps(
        {
            "text": url,
            # 'residential': residential,
            "apikey": f"{netloc_api}",
        }
    )

    netlocsmith_results = requests.post(
        f"{netloc_url}", data=post_data, headers=headers
    )
    df = pd.DataFrame(eval(json.loads(netlocsmith_results.text)))

    print(df)

    netlock_dc_results = {
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
                    "text": f"Netlock-Smith Results given below: \n\n {df}",
                },
            },
        ],
    }
    netlock_dc_resp = requests.post(
        url=response_url, headers=headers, data=json.dumps(
            netlock_dc_results)
    )
    print(netlock_dc_resp.status_code)
    return netlock_dc_resp
