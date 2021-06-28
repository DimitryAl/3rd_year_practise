
from os import X_OK


class Node:
    name = ''
    availability = 0
    def __init__(self, name, availability, coords):
        self.name = name
        self.availability = availability
        self.location = coords
    
    def change_availability(self):
        if self.availability == 0:
            self.availability = 1
        else:
            self.availability = 1

class Edge:
    weight = 1
    def __init__(self, first, second, availability, length):
        self.first = first
        self.second = second
        self.availability = availability
        self.length = length
    def change_weigth(self, x):
        self.weght = x

class Passenger:
    time_of_waiting = 0
    bus = ''
    def __init__(self, start_time, start, finish):
        self.start_time = start_time
        self.start = start
        self.finish = finish
    def change_time(self, t):
        self.time_of_waiting += t

class Route:
    nodes = []
    def __init__(self, name, nodes):
        self.name = name
        self.nodes = nodes

class Bus:
    max_pas = 20
    cur_pas = 0
    name = ''
    speed = 4
    location = 0
    start_time = 0
    def __init__(self, route, name):
        self.route = route
        self.name = name
        self.cur = 0
        self.now = self.route.nodes[self.cur]
        self.next = self.route.nodes[self.cur+1]
        self.stop = 1
        self.sign = 1
    def change_location(self, edges, time):
        for edge in edges:
            if (edge.first.name == self.now.name and edge.second.name == self.next.name):
                #self.location = edge.length - (edge.weight * self.speed) * (time - self.start_time)
                if self.location <= 0:
                    self.location = edge.length - edge.weight * self.speed
                else:
                    self.location -= edge.weight * self.speed
                if self.location <= 0:
                    self.cur += self.sign
                    if self.cur == len(self.route.nodes) - 1:
                        self.sign = -1
                    if self.cur == 0:
                        self.sign = 1
                    #self.cur += self.sign
                    self.now = self.route.nodes[self.cur]
                    self.next = self.route.nodes[self.cur+self.sign]
                    #self.start_time = time
                break
    def passenger_pickup(self, passengers):
        for passenger in passengers:
            if passenger.start.name == self.now.name:
                for node in self.route.nodes:
                    if node.name == passenger.finish.name:
                        if passenger.bus == '':
                            if self.cur_pas < self.max_pas:
                                passenger.bus = self.name
                                passenger.time_of_waiting = 0
                                self.cur_pas += 1
    def passenger_drop(self, passengers):
        for passenger in passengers:
            if passenger.bus == self.name:
                if self.now.name == passenger.finish.name:
                    passenger.bus = ''
                    self.cur_pas -= 1
                    passengers.remove(passenger)

class User:
    
    def __init__(self, location):
        self.location = location