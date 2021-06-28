
from threading import Thread
import socket
import time
import math

from classes import Node, Edge, Route, Passenger, Bus, User
from func import generate_passenger


nodes = [Node('zero', 1, [0, 0]), Node('one', 1, [10, 10]), Node('two', 1, [5, 20]), Node('three', 1, [3, 25])]
edges = [Edge(nodes[0], nodes[1], 1, 40), Edge(nodes[1], nodes[2], 1, 35), Edge(nodes[1], nodes[3], 1, 66), Edge(nodes[2], nodes[3], 1, 10), 
         Edge(nodes[1], nodes[0], 1, 40), Edge(nodes[2], nodes[1], 1, 35), Edge(nodes[3], nodes[1], 1, 66), Edge(nodes[3], nodes[2], 1, 10)]
routes = [Route('r01', [nodes[0], nodes[1], nodes[2]]), Route('r02', [nodes[1], nodes[2], nodes[3]])]
passengers = [Passenger(time, nodes[0], nodes[3]), Passenger(time, nodes[0], nodes[1]), Passenger(time, nodes[1], nodes[3])]
buses = [Bus(routes[0], 'b01'), Bus(routes[1], 'b02')]

class ServerThread(Thread):
    
    def __init__(self, name):
        Thread.__init__(self)
        self.name = name
    
    def run(self):
        
        print('Thread ', self.name, ' is running')

        serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)
        serv_sock.bind(('', 53210))
        serv_sock.listen(10)

        print('Server up and running')

        user = User('')

        while True:    
            # Бесконечно обрабатываем входящие подключения
            client_sock, client_addr = serv_sock.accept()
            print('Connected by', client_addr)

            while True:
                # Пока клиент не отключился, читаем передаваемые
                # им данные и отправляем их обратно
                data = client_sock.recv(1024)
                if not data:
                    # Клиент отключился
                    print('Client disconnect')
                    break
                else:
                    str_data = data.decode('utf-8')
                    print('Recieved data: ', str_data)
                    if str_data == 'set_location':
                        print('setting up users location')
                        client_sock.sendall('Input you location'.encode('utf-8'))
                        data = client_sock.recv(1024)
                        str_data = data.decode('utf-8')
                        user.location = str_data.split(';')
                        user.location[0] = int(user.location[0])
                        user.location[1] = int(user.location[1])
                        client_sock.sendall('Your location is set'.encode('utf-8'))
                    if str_data == 'my_location':
                        data = 'Your current location is: ' + '[' + str(user.location[0]) +  ';' + str(user.location[1]) + ']'
                        client_sock.sendall(data.encode('utf-8'))
                    if str_data == 'nearest_station':
                        min = -1
                        name = ''
                        for node in nodes:
                            if user.location == node.location:
                                data = ("You are on station " + node.name).encode('utf-8')
                                break
                            if min == -1:
                                min = math.sqrt((node.location[0] - user.location[0])**2 + (node.location[1] - user.location[1])**2)
                                name = node.name
                                data = ("Nearest station to you is " + name + ' in ' + str(min)).encode('utf-8')
                            else:
                                temp = math.sqrt((node.location[0] - user.location[0])**2 + (node.location[0] - user.location[0])**2)
                                if temp < min:
                                    min = temp
                                    name = node.name
                                    data = ("Nearest station to you is " + name + ' in ' + str(min)).encode('utf-8')
                        client_sock.sendall(data)

                    #client_sock.sendall(b'smth')

            client_sock.close()
            break

class ModelThread(Thread):

    def __init__(self, name):
        Thread.__init__(self)
        self.name = name

    def run(self):
        
        print('Thread ', self.name, ' is running')
        time = 0    #time of model
        k = 1       #time coefficient

        # nodes = [Node('zero', 1, [0, 0]), Node('one', 1, [10, 10]), Node('two', 1, [5, 20]), Node('three', 1, [3, 25])]
        # edges = [Edge(nodes[0], nodes[1], 1, 40), Edge(nodes[1], nodes[2], 1, 35), Edge(nodes[1], nodes[3], 1, 66), Edge(nodes[2], nodes[3], 1, 10), 
        #         Edge(nodes[1], nodes[0], 1, 40), Edge(nodes[2], nodes[1], 1, 35), Edge(nodes[3], nodes[1], 1, 66), Edge(nodes[3], nodes[2], 1, 10)]
        # routes = [Route('r01', [nodes[0], nodes[1], nodes[2]]), Route('r02', [nodes[1], nodes[2], nodes[3]])]
        # passengers = [Passenger(time, nodes[0], nodes[3]), Passenger(time, nodes[0], nodes[1]), Passenger(time, nodes[1], nodes[3])]
        # buses = [Bus(routes[0], 'b01'), Bus(routes[1], 'b02')]


        print('Modeling began')

        while (True):
            if time >= k*10080:                         #if week passed   
                time = 0
            if time == 100:
                break
            for bus in buses:                           #refresh every bus information
                bus.change_location(edges, time)
                bus.passenger_pickup(passengers)
                bus.passenger_drop(passengers)
            for passenger in passengers:                #refresh every passenger information
                if passenger.bus == '':
                    passenger.change_time(1)
            generate_passenger(time, passengers, nodes)
            time += 1
            #print(buses[0].name, 'pas: ', buses[0].cur_pas)
            #print(len(passengers))

        print('Modeling ended')

    


if __name__ == "__main__":
    
    # Starting thread with server 
    server_name = 'test server'
    server_thread = ServerThread(server_name)
    server_thread.start()
    time.sleep(1)

    # Starting thread with model
    model_name = 'test model'
    model_thread = ModelThread(model_name)
    model_thread.start()

