import base64
import json

import requests
import pprint
import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(".") / ".env"
print(env_path)
load_dotenv(dotenv_path=env_path)
django_user_api = os.environ["DJANGO_USER_API"]
api_url = os.environ["NETLOC_API_URL"]
netloc = input("Enter a netloc name: ")
url = f"{api_url}{netloc}"
print(url)

payload = {}
headers = {"Content-Type": "application/json"}

response = requests.request(
    "GET", url=url, auth=(django_user_api, ""), headers=headers, data=payload
)

#
res = json.loads(response.text)

print(res["count"])
if res["count"] == 0:
    print(f"No Netloc-Config for {netloc}")

else:
    # print(res['count'])
    # page2 = res['next']

    def datas(res, netloc):
        data = res["results"][0:]
        # pprint.pprint(data[0])
        # print(len(data))
        # print(len(data[0]))
        # print(data[0]['organization_name'])
        num = int(len(data))
        for n in range(num):
            # if 'Data on Demand' not in data[n]['organization_name']:
            #     print(data[n]['organization_name'])
            #     break
            # elif 'Data on Demand' in data[n]['organization_name']:
            #     pprint.pprint(data[n]['netloc_name'])
            # print(n)
            # pprint.pprint(data[n])
            dict1 = data[n]
            if "organization_name" not in dict1 and dict1["netloc_name"] == f"{netloc}":
                # print(dict1['organization_name'])
                pprint.pprint(dict1)
                f = open("netloc.json", "w")
                f.write(str(dict1))
                f.close()
                print("File Written")
                break
            else:
                print("Config does not exists")

    datas(res, netloc)
    while res["next"] is not None:
        next_page = res["next"]
        # print(f"this is line 68 {next_page}")
        response = requests.request(
            "GET",
            url=next_page,
            auth=(django_user_api, ""),
            headers=headers,
            data=payload,
        )
        # print(response.text)
        res = json.loads(response.text)
        next_page = res["next"]
        print(next_page)
        datas(res, netloc)
    # else res['next'] is None:
    #     print('Next Page Does not Exist')
