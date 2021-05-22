import socket
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

        self.BUFF_SIZE = 65536

        #audio settings
        self.CHUNK = 512
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 20000 #must match input audio device

        self.tcp_s = None
        self.udp_s = None

        self.muted = False

        self.refresh_audio_setup()

    def refresh_audio_setup(self):
        #init mic recording and sound playback
        self.p = pyaudio.PyAudio()

        inDev, outDev = self.audio_devices()
        
        inDevId = inDev[0][0]
        outDevId = outDev[0][0]

        self.rec_stream = self.p.open(format=self.FORMAT,
                        channels=self.CHANNELS,
                        rate=self.RATE,
                        input=True,
                        frames_per_buffer=self.CHUNK,
                        input_device_index=inDevId)
        self.play_stream = self.p.open(format=self.FORMAT,
                        channels=self.CHANNELS,
                        rate=self.RATE,
                        output=True,
                        frames_per_buffer=self.CHUNK,
                        output_device_index=outDevId)
    
    def in_setup(self, inDevId):
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
        defaultInputDev = self.p.get_default_input_device_info()
        defaultOutputDev = self.p.get_default_output_device_info()

        # #Choose hostapi based on system and list devices
        # if(platform.system() == 'Windows'):
        #     hostApi = self.p.get_host_api_info_by_type(pyaudio.paWASAPI)
        #     for id in range(self.p.get_device_count()):
        #         dev_dict = self.p.get_device_info_by_index(id)
        #         #if(dev_dict.get('hostApi') == hostApi.get('index')):
        #         if('SPDIF' not in dev_dict.get('name')):                    
        #             if(dev_dict.get('maxInputChannels') > 0):
        #                 inputDevs.append((dev_dict.get('index'), dev_dict.get('name')))
        #             elif(dev_dict.get('maxOutputChannels') > 0):
        #                 outputDevs.append((dev_dict.get('index'), dev_dict.get('name')))
        # else:
        #     for id in range(self.p.get_device_count()):
        #         dev_dict = self.p.get_device_info_by_index(id)
        #         if(dev_dict.get('maxInputChannels') > 0):
        #             inputDevs.append((dev_dict.get('index'), dev_dict.get('name')))
        #         elif(dev_dict.get('maxOutputChannels') > 0):
        #             outputDevs.append((dev_dict.get('index'), dev_dict.get('name')))

        #move default to first element in list
        # for i in range(len(inputDevs)):
        #     if(defaultInputDev.get('name') in inputDevs[i][1]):
        #         inputDevs.insert(0, inputDevs.pop(i))

        # for i in range(len(outputDevs)):
        #     if(defaultOutputDev.get('name') in outputDevs[i][1]):
        #         outputDevs.insert(0, outputDevs.pop(i))
        
        inputDevs.append((defaultInputDev.get('index'), defaultInputDev.get('name')))
        outputDevs.append((defaultOutputDev.get('index'), defaultOutputDev.get('name')))


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
        self.tcp_s.connect((self.server_address, self.server_tcp_port))
        data = 'JOIN ' + self.nick + ' ' + str(self.udp_s.getsockname()[1])
        self.tcp_s.send(bytes(data, 'UTF-8'))
        data = self.tcp_s.recv(1024)
        decoded = data.decode('UTF-8')
        message = decoded.split()
        if (message[0] == "OK" and len(message[1]) > 0):
            self.tcp_conn_status = True
            self.server_udp_port = int(message[1])
            #return True
        else:
            self.tcp_s.shutdown(socket.SHUT_RDWR)
            self.tcp_s.close()
            #return False

    def disconnect(self):
        self.tcp_s.send(bytes("LEAV", 'UTF-8'))
        self.tcp_s.shutdown(socket.SHUT_RDWR)
        self.tcp_s.close()
        self.tcp_conn_status = False
        print("disconnected")


    def udpSend(self):
        self.muted = False
        while True:
            if (self.tcp_conn_status == True):
                if(self.muted == False):
                    data = self.rec_stream.read(self.CHUNK, exception_on_overflow=False)
                    self.udp_s.sendto(data, (self.server_address, self.server_udp_port))
                    time.sleep(0.8*self.CHUNK/self.RATE) #time.sleep(0.8*CHUNK/sample_rate)
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
        print('connecting')
        self.tcpConnection()

        if (self.tcp_conn_status == True):
            print('connected')#zmiana na okno rozmowy
        else:
            print('error')#wyrzuć błąd
            pass
        
        Thread(target=self.udpRecv).start()
        Thread(target=self.udpSend).start()

    def mute(self):
        if(self.muted == False):
            self.muted = True
        else:
            self.muted = False
            
        return self.muted

if (__name__ == "__main__"):
    client = Client()
    client.Start('Tester', '127.0.0.1', 5001)