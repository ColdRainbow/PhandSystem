import time
import requests

TOKEN = "28c96b734e05de388719fc1b5096b7abd1ecd2355795015f97fb96f227096ab830dcfcdc621cc13f4de34"

TEXT_1 = """На Вас счёт зачислены баллы = {}
Спасибо за то, что помогаете нам и планете :)
"""

TEXT_2 = """Вы накопили много баллов = {}
"""

URL_GET = "https://api.vk.com/method/messages.getHistory"

URL_SEND = "https://api.vk.com/method/messages.send"

with open("update.txt", "r") as f:
    time_update = f.read().split()[0]
    
while True:
    with open("update.txt", "r") as f:
        time_update_new, user, value = f.read().split()
    if time_update != time_update_new:
        time_update = time_update_new
        requests.post(URL_SEND, params={"access_token": TOKEN, "v": 5.59, "user_id": user,
                                        "message": TEXT_1.format(value)})
    users = dict()
    with open("users.txt", "r") as f:
        lines = f.read().split("\n")
    for line in lines:
        if line:
            id_number = line.split()
            users[int(id_number[0])] = int(id_number[1])
    
    for user in users:
        r = requests.get(URL_GET, params={"access_token": TOKEN, "v": 5.59, "user_id": user,
                                      "count": 1 }).json()
        if "response" not in r or len(r["response"]["items"]) == 0:
            continue
        else:
            r = r["response"]
        if r["items"][0]["user_id"] == r["items"][0]["from_id"] and r["items"][0]["body"] == "Баланс":
            requests.post(URL_SEND, params={"access_token": TOKEN, "v": 5.59, "user_id": user,
                                        "message": TEXT_2.format(users[user])})
    time.sleep(2)
