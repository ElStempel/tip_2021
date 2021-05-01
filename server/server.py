import socket
from threading import Thread
from contextlib import closing

class User:
    def __init__(self, tcpConn, name, addr, udpPort):
        self.tcpConn = tcpConn
        self.name = name
        self.tcpAddr = addr
        self.udpAddr = (addr[0],udpPort)

class Server:
    def __init__(self):
        self.ip = '127.0.0.1'#socket.gethostbyname(socket.gethostname())
        self.server_udp_port = 5000
        self.server_tcp_port = 5001

        self.userList = []

        self.tcp_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_s.bind((self.ip, self.server_tcp_port))

        self.udp_s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_s.bind((self.ip, self.server_udp_port))

        print("Server is running...")
        self.userConnections()

    def userConnections(self):
        self.tcp_s.listen(25)
        while True:
            conn, address = self.tcp_s.accept()
            Thread(target=self.newConnection, args=(conn, address)).start()

    def newConnection(self, conn, address): #PORAWIĆ! KAŻDY USER POTRZEBUJE SWOJEGO PORTU UDP?
        data = conn.recv(1024) #komunikaty: JOIN Nick; LEAV;
        decoded = data.decode('UTF-8')
        message = decoded.split()
        if(message[0] == 'JOIN' and len(message[1]) > 0 and len(message[2]) > 0):
            print('Received: '+decoded+' from: '+str(address[0])+':'+str(address[1]))
            user = User(conn, message[1], address, int(message[2]))
            self.userList.append(user)
            conn.send(bytes('OK', 'UTF-8')) #można wysyłać port udp
            while True:
                self.audioStreaming()
                data = conn.recv(1024)
                decoded = data.decode('UTF-8')
                message = decoded.split()
                if(message[0] == 'LEAV'):
                    self.userList.remove(user)
                    conn.send(bytes('BYE', 'UTF-8'))
                    conn.close()
                    break
        else:
            print('Received bad data: '+decoded+' from: '+str(address[0])+':'+str(address[1]))
            conn.send(bytes('BAD DATA', 'UTF-8'))
            conn.close()

    def audioStreaming(self):
            while True:
                data, address = self.udp_s.recvfrom(2048)
                for user in self.userList:
                    if(user.udpAddr != address):
                        self.udp_s.sendto(data, user.udpAddr)

server = Server()
