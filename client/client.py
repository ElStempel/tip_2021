import socket
import pyaudio
import sys
from threading import Thread

# Socket
HOST = socket.gethostname()
MY_PORT_UDP = int(sys.argv[1])
MY_PORT_TCP = int(sys.argv[2])
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

print("Connecting from "+HOST+", TCP:"+str(MY_PORT_TCP)+", UDP:"+str(MY_PORT_UDP))

def tcpConnection():
    nick = sys.argv[3]

    with socket.socket() as tcp_socket:
        tcp_socket.bind((HOST, MY_PORT_TCP))
        tcp_socket.connect((HOST, PORT_TCP))
        #while True:
        data = 'JOIN ' + nick + ' ' + str(MY_PORT_UDP)
        tcp_socket.send(bytes(data, 'UTF-8'))
        data = tcp_socket.recv(1024)
        decoded = data.decode('UTF-8')
        print(decoded)

Thread(target=tcpConnection, args=()).start()

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
    client_socket.bind((HOST, MY_PORT_UDP))
    while True:
        data = stream.read(CHUNK)
        client_socket.sendto(data, (HOST, PORT_UDP))
        data, address = client_socket.recvfrom(PACKET_SIZE)
        stream.write(data)
        