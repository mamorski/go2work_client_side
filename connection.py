import socket
import tkinter.messagebox
import sys

ip = '37.46.36.75'

def get_connection():
    client = socket.socket()
    server_address = (ip, 1234)
    # print('connecting to {} port {}'.format(*server_address))
    client.connect(server_address)
    return client


def send_request_to_server(data_str):
    b_message = bytes(data_str, 'utf-8')
    # print(b_message)
    # print('sending {!r}'.format(data_str))
    try:
        client = get_connection()
        client.sendall(b_message)
        data = recv_msg(client)
        # data = client.recv(2048)
        # print(MSGLEN)
        if data == 'True':
            return True
        elif data == 'False':
            return False
        # print('received {!r}'.format(data))
    except Exception:
        tkinter.messagebox.showinfo("Connection", "Connection error!")
        return False
    return data


def recv_msg(sock):
    try:
        header = sock.recv(8)#Magic, small number to begin with.
        # print(header)
        # while ";" not in header:
        #     header += sock.recv(2) #Keep looping, picking up two bytes each time
        
        (size_of_package, message_fragment) = header.decode('utf-8').split(';')
        # print(type(header))
        # size_of_package, separator, message_fragment = header.partition(";")
        
        full_message = message_fragment
        # print('message is - ' + message_fragment, len(full_message), int(size_of_package))
        
       
        while True:
            if len(full_message) >= int(size_of_package):
                break
            message = sock.recv(1024)
            # print(full_message)
            full_message += message.decode('utf-8')
        # print(full_message)
        return full_message

    except OverflowError:
        return "OverflowError."
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise
