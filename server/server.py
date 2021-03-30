import socket
import pyaudio

# Socket
HOST = socket.gethostname()
PORT = 5000

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

with socket.socket() as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    conn, address = server_socket.accept()
    print("Connection from " + address[0] + ":" + str(address[1]))

    data = conn.recv(CHUNK)
    while data != "":
        data = conn.recv(CHUNK)
        #stream.write(data)
        conn.send(data)

stream.stop_stream()
stream.close()
p.terminate()