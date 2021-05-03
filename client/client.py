import socket
import pyaudio
import sys
from threading import Thread
import time
from contextlib import closing

class Client:
    def __init__(self):
        self.tcp_conn_status = False
        self.server_udp_port = 5000
        self.server_tcp_port = 5001
        self.server_address = '127.0.0.1'
        self.nick = 'Anonymous'

        #audio settings
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 20000

        #init mic recording and sound playback
        self.p = pyaudio.PyAudio()
        self.rec_stream = self.p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)
        self.play_stream = self.p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        output=True,
                        frames_per_buffer=CHUNK)

        self.tcp_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.udp_s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def set_free_udp_port(self):
        self.udp_s.bind(('', 0))

    def set_nick(self, nick):
        self.nick = nick

    def set_server_addr(self, ip):
        self.server_address = ip

    def set_server_tcp_port(self, port):
        self.server_tcp_port = port

    def tcpConnection(self):
        self.tcp_s.connect((self.server_address, self.server_tcp_port))
        #while True:
        data = 'JOIN ' + self.nick + ' ' + str(self.udp_s.getsockname()[1])
        self.tcp_s.send(bytes(data, 'UTF-8'))
        data = self.tcp_s.recv(1024)
        decoded = data.decode('UTF-8')
        if (decoded == "OK"):
            self.tcp_conn_status = True    
        else:
            self.tcp_s.shutdown(SHUT_RDWR)
            self.tcp_s.close()

    def disconnect(self):
        self.tcp_s.send(bytes("LEAV", 'UTF-8'))
        self.tcp_s.shutdown(SHUT_RDWR)
        self.tcp_s.close()
        self.tcp_conn_status = False


    def udpSend(self):
        while True:
            if (self.tcp_conn_status == True):
                data = self.rec_stream.read(1024)
                self.udp_s.sendto(data, (self.server_address, self.server_udp_port))
                time.sleep(0.8*1024/20000) #time.sleep(0.8*CHUNK/sample_rate)
            else:
                break

    def udpRecv(self):
        while True:
            if (self.tcp_conn_status == True):
                data, addr = self.udp_s.recvfrom(2048)
                self.play_stream.write(data)
            else:
                break

    def Start(self, nick, server_addr, server_tcp_port):
        self.set_free_udp_port()
        self.set_nick(nick)
        self.set_server_addr(server_addr)
        self.set_server_tcp_port(server_tcp_port)
        print('connecting')
        self.tcpConnection()#napisać obsługę braku połączenia

        if (self.tcp_conn_status == True):
            print('connected')#zmiana na okno rozmowy
        else:
            print('error')#wyrzuć błąd
            pass
        
        recv_thread = Thread(target=self.udpRecv).start()
        self.udpSend()

if (__name__ == "__main__"):
    client = Client()
    client.Start()