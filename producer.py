import socket
import sys

cont = 'Y'
topic = sys.argv[1]

while cont == 'Y':
    s = socket.socket()
    host = socket.gethostname()
    port = 9500
    s.connect((host, port))

    message = input("Enter a Message: ")

    s.send(bytes(topic+"$:$"+message, "utf-8"))

    print(f"Sent message \"{message}\" to broker.")
    
    cont = input("Sent another message? (Y/N): ")