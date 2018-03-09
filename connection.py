import socket


def get_connection():
    client = socket.socket()
    server_address = ('192.168.43.46', 1234)
    print('connecting to {} port {}'.format(*server_address))
    client.connect(server_address)
    return client


def send_request_to_server(data_str):
    b_message = bytes(data_str, 'utf-8')
    print(b_message)
    print('sending {!r}'.format(data_str))
    try:
        client = get_connection()
        client.sendall(b_message)
        data = client.recv(1024)
        print('received {!r}'.format(data))
    except Exception:
        print("Connection failed")
    return data
