from os import error
import socket
import select
import sounddevice as sd
import pyaudio
import sys
from threading import Thread
import time
from contextlib import closing
import platform

class Client:
    def __init__(self):
        self.tcp_conn_status = False
        self.server_udp_port = None
        self.server_tcp_port = None
        self.server_address = '127.0.0.1'
        self.nick = 'Anonymous'

        self.guiMessage = 0

        self.BUFF_SIZE = 65536

        #audio settings
        self.CHUNK = 32
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100

        self.tcp_s = None
        self.udp_s = None

        self.muted = False
        self.usersList = []
        self.p = pyaudio.PyAudio()
        self.refresh_audio_setup()

    def refresh_audio_setup(self):
        #init mic recording and sound playback
        
        sd._terminate()
        sd._initialize()

        inDev, outDev = self.audio_devices()
        
        try:
            inDevId = inDev[0][0]
            self.rec_stream = self.p.open(format=self.FORMAT,
                            channels=self.CHANNELS,
                            rate=self.RATE,
                            input=True,
                            frames_per_buffer=self.CHUNK,
                            input_device_index=inDevId)
        except:
            pass

        try:    
            outDevId = outDev[0][0]
            self.play_stream = self.p.open(format=self.FORMAT,
                            channels=self.CHANNELS,
                            rate=self.RATE,
                            output=True,
                            frames_per_buffer=self.CHUNK,
                            output_device_index=outDevId)
        except:
            pass

        return inDev, outDev
    
    def in_setup(self, inDevId):
        print(inDevId)
        try:
            self.rec_stream = self.p.open(format=self.FORMAT,
                            channels=self.CHANNELS,
                            rate=self.RATE,
                            input=True,
                            frames_per_buffer=self.CHUNK,
                            input_device_index=inDevId)
        except:
            pass
        
    def out_setup(self, outDevId):
        print(outDevId)
        try:
            self.play_stream = self.p.open(format=self.FORMAT,
                        channels=self.CHANNELS,
                        rate=self.RATE,
                        output=True,
                        frames_per_buffer=self.CHUNK,
                        output_device_index=outDevId)
        except:
            pass

    def audio_devices(self):
        inputDevs = []
        outputDevs = []
        
        #Choose hostapi based on system and list devices
        if(platform.system() == 'Windows'):
            hostApi = self.p.get_host_api_info_by_type(pyaudio.paMME)
            for id in range(len(sd.query_devices())):
                dev_dict = sd.query_devices(device=id)
                if(dev_dict.get('hostapi') == hostApi.get('index')):
                    if('SPDIF' not in dev_dict.get('name')):                    
                        if(dev_dict.get('max_input_channels') > 0):
                            inputDevs.append((id, dev_dict.get('name')))
                        elif(dev_dict.get('max_output_channels') > 0):
                            outputDevs.append((id, dev_dict.get('name')))
        else:
            for id in range(len(sd.query_devices())):
                dev_dict = sd.query_devices(device=id)
                if('SPDIF' not in dev_dict.get('name')):                    
                    if(dev_dict.get('max_input_channels') > 0):
                        inputDevs.append((id, dev_dict.get('name')))
                    elif(dev_dict.get('max_output_channels') > 0):
                        outputDevs.append((id, dev_dict.get('name')))

        #Move default to first element in list

        try:
            defaultInputDev = sd.default.device[0]
            for i in range(len(inputDevs)):
                if(inputDevs[i][0] == defaultInputDev):
                    inputDevs.insert(0, inputDevs.pop(i))
        except:
            self.guiMessage = 2

        try:
            defaultOutputDev = sd.default.device[1]
            for i in range(len(outputDevs)):
                if(outputDevs[i][0] == defaultOutputDev):
                    outputDevs.insert(0, outputDevs.pop(i))
        except:
            self.guiMessage = 3

        return inputDevs, outputDevs

    def sockets_setup(self):
        self.tcp_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.udp_s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_s.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,self.BUFF_SIZE)
        self.udp_s.bind(('', 0))
        self.udp_s.settimeout(0.2)
        self.tcp_s.settimeout(1)

    def set_nick(self, nick):
        self.nick = nick

    def set_server_addr(self, ip):
        self.server_address = ip

    def set_server_tcp_port(self, port):
        self.server_tcp_port = port

    def tcpConnection(self):
        data = 'JOIN ' + self.nick + ' ' + str(self.udp_s.getsockname()[1])
        self.tcp_s.send(bytes(data, 'UTF-8'))
        data = self.tcp_s.recv(1024)
        decoded = data.decode('UTF-8')
        message = decoded.split()
        if (message[0] == "OK" and len(message[1]) > 0):
            self.tcp_conn_status = True
            self.server_udp_port = int(message[1])
            #Start voice voice streaming
            Thread(target=self.udpRecv).start()
            Thread(target=self.udpSend).start()
        else:
            self.tcp_s.shutdown(socket.SHUT_RDWR)
            self.tcp_s.close()

        while(self.tcp_conn_status == True):
            #check if everything is ok
            try:
                ready_to_read, ready_to_write, in_error = \
                    select.select([self.tcp_s,], [self.tcp_s,], [], 5)
            
                if len(ready_to_read) > 0:
                    recv = self.tcp_s.recv(1024)
                    decoded = recv.decode('UTF-8')
                    message = decoded.split()
                    if (message[0] == "LIST"):
                        users = []
                        for i in range(1, len(message)):
                            users.append(message[i])
                        self.usersList = users

                if len(ready_to_write) > 0:
                    self.tcp_s.send(bytes('AWLI', 'UTF-8'))

                time.sleep(1)

            except:
                if(self.tcp_conn_status == True):
                    try:
                        self.tcp_s.shutdown(socket.SHUT_RDWR)
                        self.tcp_s.close()
                        self.tcp_conn_status = False
                        self.guiMessage = 1
                    except:
                        self.tcp_s.close()
                        self.tcp_conn_status = False
                        self.guiMessage = 1
                break

    def disconnect(self):
        try:
            self.tcp_s.send(bytes("LEAV", 'UTF-8'))
            recv = self.tcp_s.recv(1024)
            decoded = recv.decode('UTF-8')
            if(decoded == 'BYE'):
                self.tcp_s.shutdown(socket.SHUT_RDWR)
                self.tcp_s.close()
            self.tcp_conn_status = False
        except:
            self.tcp_s.close()
            self.tcp_conn_status = False
        print("disconnected")


    def udpSend(self):
        while True:
            if (self.tcp_conn_status == True):            
                try:
                    if(self.muted == False):
                        data = self.rec_stream.read(self.CHUNK, exception_on_overflow=False)
                    else:
                        data = b''
                    self.udp_s.sendto(data, (self.server_address, self.server_udp_port))
                except:
                    pass
            else:
                break
            
    def udpRecv(self):
        while True:
            if (self.tcp_conn_status == True):
                try:
                    data, addr = self.udp_s.recvfrom(2048)
                    self.play_stream.write(data)
                except:
                    pass
            else:
                break

    def Start(self, nick, server_addr, server_tcp_port):
        self.sockets_setup()
        self.set_nick(nick)
        self.set_server_addr(server_addr)
        self.set_server_tcp_port(server_tcp_port)
        self.muted = False
        self.usersList = []
        print('connecting')
        self.tcp_s.connect((self.server_address, self.server_tcp_port))
        print('connected')
        Thread(target=self.tcpConnection).start()

    def mute(self):
        if(self.muted == False):
            self.muted = True
        else:
            self.muted = False
            
        return self.muted

if (__name__ == "__main__"):
    client = Client()
    client.Start('Tester', '127.0.0.1', 5001)