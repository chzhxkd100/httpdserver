import socket

HOST = '127.0.0.1'
PORT = 8080

text = input('Input text: ').strip()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(text.encode('utf-8'))
    data = s.recv(1500)
    data = data.decode('utf-8')
    
print(f'Received {data}')
