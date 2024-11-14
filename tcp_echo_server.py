import socket
HOST = ''
PORT = 8080

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    print('start server')
    while True:
        try:
            conn, addr = s.accept()
            with conn:
                print('Connected by ', addr)
                while True:
                    data = conn.recv(1500)
                    if not data:
                        break
                    conn.sendall(data)
        except KeyboardInterrupt:
            print("Shutdown Server")
            break