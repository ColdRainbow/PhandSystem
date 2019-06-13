import requests

TOKEN = "28c96b734e05de388719fc1b5096b7abd1ecd2355795015f97fb96f227096ab830dcfcdc621cc13f4de34"


URL_GET = "https://api.vk.com/method/messages.getHistory"

URL_SEND = "https://api.vk.com/method/messages.send"


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
    return litter


def litter_to_containers(robot, containers, sorting, litter): # Распределяет по контейнерам с помощью робота
    for litter_id, litter_type, litter_mass in litter:  # Распаковка кортежа
        if litter_type in sorting:
            container = sorting[litter_type]  # В словаре для сортировки находим контейнер, в который нужно положить, по типу мусора
            containers[container] += litter_mass
            item = litter_id, litter_type, litter_mass
            robot.move_to_container(item, container)
        else:
            robot.eject(item)
            
    
def check_overfill_new(containers):
    overfilled = dict()
    for containers, total_mass in containers.items():
        if total_mass >= max_mass:
            overfilled[containers] = total_mass
    requests.post(URL_SEND, params={"access_token": TOKEN, "v": 5.59, "user_id": 231847345, "message": str(overfilled)})
    
    


def save_containers(containers, file_name): # Сохраняет на диск текущее состояние контейнера
    with open(file_name, 'w') as file:
        for container, total_mass in containers.items():
            file.write(f'{container} {total_mass}\n')



containers = get_containers('containers.txt')
sorting, bonuses = get_sorting('litter_to_containers.txt')
litter = get_litter('litter.txt', "litter_mass.txt")
litter_to_containers(robot, containers, sorting, litter)
check_overfill_new(containers)
save_containers(containers, 'containers.txt')
