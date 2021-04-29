import socket
import pyaudio
import sys
from threading import Thread
import time
from contextlib import closing

tcp_conn_status = False
disconnect = False

# Socket
def find_free_tcp_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]

def find_free_udp_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_DGRAM)) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]

HOST = socket.gethostname()
MY_PORT_UDP = find_free_udp_port()
MY_PORT_TCP = find_free_tcp_port()
PORT_UDP = 5000
PORT_TCP = 5001
PACKET_SIZE = 1024 * 8


# Audio
CHUNK = 1024 * 4
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                output=True,
                frames_per_buffer=CHUNK)


def tcpConnection():
    nick = "STMPL"#sys.argv[3]
    global tcp_conn_status
    global disconnect

    with socket.socket() as tcp_socket:
        tcp_socket.bind((HOST, MY_PORT_TCP))
        tcp_socket.connect((HOST, PORT_TCP))
        #while True:
        data = 'JOIN ' + nick + ' ' + str(MY_PORT_UDP)
        tcp_socket.send(bytes(data, 'UTF-8'))
        data = tcp_socket.recv(1024)
        decoded = data.decode('UTF-8')
        if (decoded == "OK"):
            tcp_conn_status = True
            while True:
                if (disconnect == True):
                    tcp.socket.send(bytes("LEAV", 'UTF-8'))
                    tcp_socket.shutdown(SHUT_RDWR)
                    tcp_socket.close()
                    break
        else:
            tcp_socket.shutdown(SHUT_RDWR)
            tcp_socket.close()
        tcp_conn_status = False


def udpConnection():
    global tcp_conn_status
    global disconnect
    while True:
        if (tcp_conn_status == True):
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
                client_socket.bind((HOST, MY_PORT_UDP))
                while (disconnect == False):
                    data = stream.read(CHUNK)
                    client_socket.sendto(data, (HOST, PORT_UDP))
                    data, address = client_socket.recvfrom(PACKET_SIZE)
                    stream.write(data)

tcpThread = Thread(target=tcpConnection, args=())
udpThread = Thread(target=udpConnection, args=())

def Start():
    global tcp_conn_status
    global disconnect
    tcpThread.start()
    for i in range(10):
        print('connecting')#komunikat "connecting"
        if (tcp_conn_status == True):
            break
        time.sleep(1)
    if (tcp_conn_status == True):
        udpThread.start()
        print('connected')#zmiana na okno rozmowy
    else:
        print('error')#wyjeb błąd
        pass

def stopConnection():
    global tcp_conn_status
    global disconnect
    disconnect = True
    while (disconnect == True):
        if (tcp_conn_status == False):
            disconnect = False

if (__name__ == "__main__"):
    Start()