import socket
import sys

topic = sys.argv[1]

s = socket.socket()
host = socket.gethostname()
port = 9600
s.connect((host, port))

s.send(bytes(topic, "utf-8"))

message = str(s.recv(1024), "utf-8")

print(f"BROKER:\n{message}")

s.close()