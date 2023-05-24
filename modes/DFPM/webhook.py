from fastapi import FastAPI, Request, Response
import http
import formatter
import random
import string
import time

app = FastAPI()


@app.post("/webhook", status_code=http.HTTPStatus.ACCEPTED)
async def webhook(request: Request):
    payload = await request.json()
    # print(payload)
    # with open("payload_old.json", "w") as f:
    #     f.write(str(payload))
    #
    # org_id = formatter.formatter(str(payload))
    # print(org_id)

    # len_of_chars = 8
    # filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=len_of_chars))
    #
    # full_name = '/home/mukthy/Desktop/DFPM/' + filename + '.json'
    #
    # # payload = payload.replace("'", '"')
    # print(payload)
    #
    # with open(f"{full_name}", "w") as f:
    #     f.write(str(payload))

    fingerprint_list = []
    print(len(payload))

    for i in range(len(payload)):
        if 'warning' == payload[i]['level']:
            print(payload[i]['level'])
            print(payload[i]['category'])
            data = {
                payload[i]['level']: payload[i]['category'],
                'url': payload[i]['url']
            }
            fingerprint_list.append(data)

        elif 'danger' == payload[i]['level']:
            print(payload[i]['level'])
            print(payload[i]['category'])
            print(payload[i]['url'])
            data = {
                payload[i]['level']: payload[i]['category'],
                'url': payload[i]['url']
            }
            fingerprint_list.append(data)

    else:
        print('No Fingerprint')

    print(fingerprint_list)
    unique_list = [dict(s) for s in set(frozenset(d.items()) for d in fingerprint_list)]
    data = {
        "fingerprint": unique_list
    }
    print(data)
    with open("final_data.json", "w") as f:
        f.write(str(data))
    return data


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=8000)
