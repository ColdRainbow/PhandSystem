from robot import Robot

import time
import requests


max_mass = 10000

def get_containers(file_name): #Читает файл с информацией о том, какие контейнеры бывают, сколько в них мусора находится
    containers = dict()
    with open(file_name, 'r') as file:
        for line in file:
            container, total_mass = line.strip().split()
            containers[container] = int(total_mass)
    return containers


def get_sorting(file_name): #Читает файл, в котором написано, как что сортируется, возвращает номер мусора, контейнер и бонусы
    sorting, bonuses = dict(), dict()
    with open(file_name, 'r') as file:
        for line in file:
            litter_type, container, bonus = line.strip().split()
            sorting[int(litter_type)] = container
            bonuses[int(litter_type)] = bonus
    return sorting, bonuses


def get_litter(litter_file_name, mass_file_name): #Читает из файла массы, тип мусора
    mass, litter = dict(), list()
    with open(mass_file_name, 'r') as file:
        for line in file:
            litter_id, litter_mass = line.strip().split()
            mass[int(litter_id)] = int(litter_mass)
    with open(litter_file_name, 'r') as file:
        for line in file:
            line = line.strip()  # Чтоб очистить от символа, обозначающего конец строки
            litter_id, litter_type = (int(line[-6:-1]), int(line[-1]))
            litter_mass = mass[litter_id]
            litter.append((litter_id, litter_type, litter_mass))
    return litter, mass


def check_overfill(containers):
    overfilled = dict()
    for containers, total_mass in containers.items():
        if total_mass >= max_mass:
            overfilled[containers] = total_mass
    requests.post('https://pfandsystem.pythonanywhere.com/overfilled', json=overfilled)


def save_containers(containers, file_name): # Сохраняет на диск текущее состояние контейнера
    with open(file_name, 'w') as file:
        for container, total_mass in containers.items():
            file.write(f'{container} {total_mass}\n')


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


robot = Robot()
containers = get_containers('containers.txt')
sorting, bonuses = get_sorting('litter_to_containers.txt')
litter, mass = get_litter('litter.txt', "litter_mass.txt")


while True:
    user = int(input("Введите свой ID: "))
    update_users(user, 0)
    strich = int(input("Вставьте мусор:"))
    litter_id, litter_type = (int(strich[-6:-1]), int(strich[-1]))
    litter_mass = mass[litter_id]
    if litter_type in sorting:
        container = sorting[
            litter_type]  # В словаре для сортировки находим контейнер, в который нужно положить, по типу мусора
        containers[container] += litter_mass
        item = litter_id, litter_type, litter_mass
        robot.move_to_container(item, container)
    else:
        robot.eject(item)
    check_overfill(containers)
    save_containers(containers, 'containers.txt')
