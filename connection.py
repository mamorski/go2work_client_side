import socket
import tkinter.messagebox
import sys

# global ip
ip = '192.168.1.5'
port = 1234

# connect to server function
# create socket and connect to server
def get_connection():
    client = socket.socket()
    server_address = (ip, port)
    client.connect(server_address)
    return client

# send and receive data to/from server
# receive message by recv_msg(sock)
def send_request_to_server(data_str):
    b_message = bytes(data_str, 'utf-8')
    try:
        client = get_connection()
        client.sendall(b_message)
        data = recv_msg(client)
        if data == 'True':
            return True
        elif data == 'False':
            return False
    except Exception:
        # tkinter.messagebox.showinfo("Connection", "Connection error!")
        return False
    return data

# receive message function
# implement protocol of getting (size of message);(message) 
# receive message in parts of 1024 bits
def recv_msg(sock):
    try:
        header = sock.recv(8) # Magic, small number to begin with.
        (size_of_package, message_fragment) = header.decode('utf-8').split(';')        
        full_message = message_fragment
        while True:
            if len(full_message) >= int(size_of_package):
                break
            message = sock.recv(1024)
            full_message += message.decode('utf-8')
        return full_message
    except OverflowError:
        return "OverflowError."
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise
