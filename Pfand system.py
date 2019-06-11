import time
def update_users(user, value):
    users = dict()
    with open("users.txt", "r") as f:
        lines = f.read().split("\n")
    for line in lines:
        if line:
            id_number = line.split()
            users[int(id_number[0])] = int(id_number[1])
    
    if value > 0:
        with open("update.txt", "w") as f:
            f.write("{} {} {}".format(time.time(), user, value))
    
    if user not in users:
        users[user] = 0
    users[user] += value
    
    with open("users.txt", "w") as f:
        for user in users.keys():
            f.write("{} {}\n".format(user, users[user]))
