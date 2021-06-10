<<<<<<< HEAD
import random

from classes import Passenger


def generate_passenger(time, passengers, nodes):
    if random.randint(0, 100) > 20:
        return 0
    rand_start = random.randint(0, len(nodes)-1)
    rand_finish = random.randint(0, len(nodes)-1)
    while rand_finish == rand_start:
        rand_finish = random.randint(0, len(nodes) - 1)
    passengers.append(Passenger(time, nodes[rand_start], nodes[rand_finish]))    
    return 1
=======
import random

from classes import Passenger


def generate_passenger(time, passengers, nodes):
    if random.randint(0, 100) > 20:
        return 0
    rand_start = random.randint(0, len(nodes)-1)
    rand_finish = random.randint(0, len(nodes)-1)
    while rand_finish == rand_start:
        rand_finish = random.randint(0, len(nodes) - 1)
    passengers.append(Passenger(time, nodes[rand_start], nodes[rand_finish]))    
    return 1
>>>>>>> 83a001f12a3f0c19d7407aba8ad5e3a2f2143742
