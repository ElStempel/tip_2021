import socket
from threading import Thread
from contextlib import closing
import sys, re
import time
class User:
    def __init__(self, tcpConn, name, addr, udpPort):
        self.tcpConn = tcpConn
        self.name = name
        self.tcpAddr = addr
        self.udpAddr = (addr[0],udpPort)

class Server:
    def __init__(self, ip, tcp_port):
        if(ip.lower() == 'auto' or ip == ''):
            self.ip = socket.gethostbyname(socket.gethostname())
        else:
            self.ip = ip

        if(tcp_port.lower() == 'auto' or tcp_port == ''):
            self.server_tcp_port = 0
        else:
            self.server_tcp_port = int(tcp_port)


        #self.server_udp_port = 5000 #do zmiany, będzie wysyłanie w połączeniu tcp
        
        self.userList = []

        self.tcp_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_s.bind((self.ip, self.server_tcp_port))
        self.server_tcp_port = self.tcp_s.getsockname()[1]

        self.udp_s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_s.bind((self.ip, 0))

        print("Server is listening on "+self.ip+':'+str(self.server_tcp_port)+" ...")
        self.userConnections()

    def userConnections(self):
        self.tcp_s.listen(25)
        Thread(target=self.sendUserList).start()
        while True:
            conn, address = self.tcp_s.accept()
            Thread(target=self.newConnection, args=(conn, address)).start()

    def newConnection(self, conn, address):
        data = conn.recv(1024) #komunikaty: JOIN Nick; LEAV;
        decoded = data.decode('UTF-8')
        message = decoded.split()
        if(message[0] == 'JOIN' and len(message[1]) > 0 and len(message[2]) > 0):
            
            user = User(conn, message[1], address, int(message[2]))
            self.userList.append(user)

            #create udp socket for user
            user_udp_s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            user_udp_s.bind((self.ip, 0))

            #send OK with udp port for audio communication
            conn.send(bytes('OK '+str(user_udp_s.getsockname()[1]), 'UTF-8'))
            print("\n"+user.udpAddr[0]+" User "+user.name+" joined server")
            print("  TCP: "+str(user.tcpAddr[1])+" <-> "+str(self.server_tcp_port))
            print("  UDP: "+str(user.udpAddr[1])+" <-> "+str(user_udp_s.getsockname()[1]))
            
            Thread(target=self.audioStreaming, args=(user_udp_s, user)).start()

            while True:
                try:
                    data = conn.recv(1024)
                    decoded = data.decode('UTF-8')
                    message = decoded.split()
                    if(message[0] == 'LEAV'):
                        self.userList.remove(user)
                        conn.send(bytes('BYE', 'UTF-8'))
                        print("\nUser "+user.name+" from: "+user.udpAddr[0]+":"+str(user.tcpAddr[1])+" disconnected peacefully")
                        conn.close()
                        break
                except socket.error:
                    self.userList.remove(user)
                    print("\nUser "+user.name+" from: "+user.udpAddr[0]+":"+str(user.tcpAddr[1])+" disconnected forcibly")
                    conn.close()
                    break
        else:
            print('\nReceived bad data: '+decoded+' from: '+str(address[0])+':'+str(address[1]))
            conn.send(bytes('BAD DATA', 'UTF-8'))
            conn.close()

    def audioStreaming(self, soc, streamer):
        while streamer in self.userList:
            data, address = soc.recvfrom(2048)
            for user in self.userList:
                if(user.udpAddr != address):
                    self.udp_s.sendto(data, user.udpAddr)

    def sendUserList(self):
        while True:
            time.sleep(1)
            users = []
            for user in self.userList:
                users.append(user.name)
            for user in self.userList:
                user.tcpConn.send(bytes('LIST '+str(users), 'UTF-8'))

file_problem = False
ip_regex = "^(?:(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])\.){3}(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])$"

try:
    file = open("config.txt", "r")
    content = file.read().splitlines()
    ip = content[0]
    tcp_port = content[1]
    file.close()
    if(ip.lower() != 'auto' and ip != '' and not re.search(ip_regex, ip)):
        raise ValueError('Wrong IP address')
    if(tcp_port.lower() != 'auto' and tcp_port != '' and (int(tcp_port) > 65535 or int(tcp_port) < 1)):
        raise ValueError('Wrong port')
except ValueError as er:
    print("Config error: "+str(er)+"\nProper config.txt file:\n   1st line is server IP (you may use 'auto' or '')\n   2nd line is server port to listen on (you may use 'auto' or '')")
    input()
    file_problem = True
except:
    print("Missing proper config.txt file:\n   1st line is server IP (you may use 'auto' or '')\n   2nd line is server port to listen on (you may use 'auto' or '')")
    input()
    file_problem = True

if(not file_problem):
    server = Server(ip, tcp_port)
