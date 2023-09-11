import socket
import os
from threading import Thread

def store_message(topic, message):
    if not os.path.exists(os.path.join(os.getcwd(), topic)):
        os.mkdir(os.path.join(os.getcwd(), topic))
    
    file_object = open(f'{topic}/messages.txt', 'a')
    file_object.write(message + "\n")
    file_object.close()

def retrieve_messages(topic):
    if not os.path.exists(os.path.join(os.getcwd(), topic)):
        os.mkdir(os.path.join(os.getcwd(), topic))
        file_obj = open(f"{topic}/messages.txt", "w")
        file_obj.close()
    
    file_obj = open(f"{topic}/messages.txt", "r")
    message = file_obj.read()
    file_obj.close()
    return message

def producer_connect(prod_sock):
    while True:
        pro_c, pro_addr = prod_sock.accept()
        print(f"Got connection from producer at {pro_addr}")
        top_message = str(pro_c.recv(1024), "utf-8")
        topic = top_message[:top_message.find('$:$')]
        message = top_message[top_message.find('$:$')+3:]
        store_message(topic, message)
        print(f"PRODUCER{pro_addr}: \"{message}\"")
        pro_c.close()

def consumer_connect(cons_sock):
    while True:
        con_c, con_addr = cons_sock.accept()
        print(f"Got connection from consumer at {con_addr}")
        topic = str(con_c.recv(1024), "utf-8")
        cons_msg = retrieve_messages(topic) 
        con_c.send(bytes(cons_msg, "utf-8"))
        print(f"Sent message to consumer.")
        con_c.close()


prod_sock = socket.socket()
prod_host = socket.gethostname()
prod_port = 9500
prod_sock.bind((prod_host, prod_port))

cons_sock = socket.socket()
cons_host = socket.gethostname()
cons_port = 9600
cons_sock.bind((cons_host, cons_port))

prod_sock.listen(5)
cons_sock.listen(5)

prod_thread = Thread(target = lambda : producer_connect(prod_sock))
cons_thread = Thread(target = lambda : consumer_connect(cons_sock))
prod_thread.start()
cons_thread.start()