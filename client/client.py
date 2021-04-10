import socket
import pyaudio

# Socket
HOST = socket.gethostname()
PORT = 5000
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

print("Recording")

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
    client_socket.bind((HOST, 5001))
    #client_socket.connect((HOST, PORT))
    while True:
        data = stream.read(CHUNK)
        client_socket.sendto(data, (HOST, PORT))
        data, address = client_socket.recvfrom(PACKET_SIZE)
        stream.write(data)
        