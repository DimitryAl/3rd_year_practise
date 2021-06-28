import socket
import random
from tkinter import *




def main():

    def clicked1():
        client_sock.sendall("nearest_station".encode('utf-8'))
        data = client_sock.recv(1024)
        lbl2 = Label(window, text=data.decode('utf-8'))
        lbl2.grid(column=1, row=1)

    def clicked2():
        client_sock.sendall("bus_list".encode('utf-8'))
        data = client_sock.recv(1024)
        list = data.decode('utf-8').split(';')
        lb2 = Listbox(height=5)
        for i in list:
            lb2.insert(0,i)
        lb2.grid(column=1, row=2)

    def clicked3():
        client_sock.sendall("station_list".encode('utf-8'))
        data = client_sock.recv(1024)
        list = data.decode('utf-8').split(';')
        lb3 = Listbox(height=5)
        for i in list:
            lb3.insert(0,i)
        lb3.grid(column=1, row=3)

    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect(('127.0.0.1', 53210))
    
    client_sock.sendall("set_location".encode('utf-8'))
    data = client_sock.recv(1024)
    print('Received: ', data.decode('utf-8'))
    x = str(random.randint(0, 15))
    y = str(random.randint(0, 15))
    coordinats = x + ';' + y
    client_sock.sendall(coordinats.encode('utf-8'))
    data = client_sock.recv(1024)
    print('Received: ', data.decode('utf-8'))

    window = Tk()
    window.title('Demo')
    window.geometry("500x250+300+300")
    lbl1 = Label(window, text='Ваши координаты: ' + x + ';' + y)
    lbl1.grid(column=0, row=0)
    btn1 = Button(window, text="Показать ближайшую остановку", command=clicked1)  
    btn1.grid(column=0, row=1)  
    btn2 = Button(window, text="Вывести список автобусов", command=clicked2)  
    btn2.grid(column=0, row=2)  
    btn3 = Button(window, text="Вывести список всех остановок", command=clicked3)  
    btn3.grid(column=0, row=3)  
    window.mainloop()  

    # while True:
    #     message = input()
    #     if message == 'exit':
    #         client_sock.close()
    #         break
    #     client_sock.sendall(message.encode('utf-8'))
    #     data = client_sock.recv(1024)
    #     print('Received', repr(data))


if __name__ == '__main__':

    main()
