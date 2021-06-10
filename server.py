
from threading import Thread
import socket

from classes import Node, Edge, Route, Passenger, Bus
from func import generate_passenger

def ServerThread(Thread):
    
    def __init__(self, name):
        Thread.__init__(self)
        self.name = name
    
    def run(self):
        
        print('Thread ', self.name, ' is running')

        serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)
        serv_sock.bind(('', 53210))
        serv_sock.listen(10)

        print('Server up and running')

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
                str_data = data.decode('utf-8')
                #print('Recieved data: ', str_data)
                client_sock.sendall(data)

            client_sock.close()
            break

def ModelThread(Thread):

    def __init__(self, name):
        Thread.__init__(self)
        self.name = name

    def run(self):
        
        print('Thread ', self.name, ' is running')
        time = 0    #time of model
        k = 1       #time coefficient

        nodes = [Node('one', 1), Node('two', 1), Node('three', 1), Node('four', 1)]
        edges = [Edge(nodes[0], nodes[1], 1, 40), Edge(nodes[1], nodes[2], 1, 35), Edge(nodes[1], nodes[3], 1, 66), Edge(nodes[2], nodes[3], 1, 10), 
                Edge(nodes[1], nodes[0], 1, 40), Edge(nodes[2], nodes[1], 1, 35), Edge(nodes[3], nodes[1], 1, 66), Edge(nodes[3], nodes[2], 1, 10)]
        routes = [Route('r01', [nodes[0], nodes[1], nodes[2]]), Route('r02', [nodes[1], nodes[2], nodes[3]])]
        passengers = [Passenger(time, nodes[0], nodes[3]), Passenger(time, nodes[0], nodes[1]), Passenger(time, nodes[1], nodes[3])]
        buses = [Bus(routes[0], 'b01'), Bus(routes[1], 'b02')]


        print('Modeling began')

        while (True):
            if time >= k*10080:                         #if week passed   
                time = 0
            if time == 1000:
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

        print('Modeling ended')

    


if __name__ == "__main__":
    print('Program start\n')
    server_name = 'test server'
    server_thread = ServerThread(server_name)
    print(type(server_thread))
    server_thread.start()
    # model_name = 'test model'
    # model_thread = ModelThread(model_name)
    # model_thread.start()
    print('Program end\n')