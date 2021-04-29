import socket
import pyaudio
from threading import Thread
from users import User

# Participants List
userList = []

# Socket
HOST = socket.gethostname()
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
                output=True,
                frames_per_buffer=CHUNK)

print("Server is running...")

def newConnection(conn, address): #PORAWIĆ! KAŻDY USER POTRZEBUJE SWOJEGO PORTU TCP
    data = conn.recv(1024) #komunikaty: JOIN Nick; LEAV;
    decoded = data.decode('UTF-8')
    message = decoded.split()
    if(message[0] == 'JOIN' and len(message[1]) > 0 and len(message[2]) > 0):
        print('Received: '+decoded+' from: '+str(address[0])+':'+str(address[1]))
        user = User(conn, message[1], address, int(message[2]))
        userList.append(user)
        conn.send(bytes('OK', 'UTF-8'))
        while True:
            data = conn.recv(1024)
            decoded = data.decode('UTF-8')
            message = decoded.split()
            if(message[0] == 'LEAV'):
                userList.remove(user)
                conn.send(bytes('BYE', 'UTF-8'))
                conn.close()
    else:
        print('Received bad data: '+decoded+' from: '+str(address[0])+':'+str(address[1]))
        conn.send(bytes('BAD DATA', 'UTF-8'))
        conn.close()


def userConnections():
    with socket.socket() as connection_socket:
        connection_socket.bind((HOST, PORT_TCP))
        connection_socket.listen(25)

        while True:
            conn, address = connection_socket.accept()
            Thread(target=newConnection, args=(conn, address)).start()
            

def audioStreaming():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.bind((HOST, PORT_UDP))

        while True:
            data, address = server_socket.recvfrom(PACKET_SIZE)
            for user in userList:
                if(user.udpAddr != address):
                    server_socket.sendto(data, user.udpAddr)

t1 = Thread(target=userConnections, args=())
t2 = Thread(target=audioStreaming, args=())
t1.start()
t2.start()

stream.stop_stream()
stream.close()
p.terminate()