import os
import socket
import mimetypes  # MIME 타입을 자동으로 인식하기 위한 모듈
HOST = ''
PORT = 8888
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(10)
    print('Start server')
    while True:
        try:
            conn, addr= s.accept()
            with conn:
                print(f'Connected by {addr}')
                
                data =conn.recv(1500)
                if not data:
                    break
                
                # 요청 데이터의 첫 번째 줄을 파싱
                try:
                    request_line = data.decode('utf-8').splitlines()[0]
                    method, path, protocol = request_line.split(' ', 2)  # 최대 2개의 공백으로 분리하여 안전하게 처리
                except (ValueError, IndexError) as e:
                    print(f"Error parsing request line: {e}")
                    # 잘못된 요청 형식일 때 처리
                    conn.sendall(b'HTTP/1.1 400 Bad Request\r\n\r\n')
                    continue
                
                print(f'Received: {method} {path} {protocol}')

                if path == '/':
                    path = '/index.html'
                path = f'.{path}'
                if not os.path.exists(path):
                    header ='HTTP/1.1 404 Not Found\r\n'
                    header =f'{header}Server: Our server\r\n'
                    header =f'{header}Connection: close\r\n'
                    header =f'{header}Content-Type: text/html;charset=utf-8\r\n'
                    header =f'{header}\r\n'
                    header =header.encode('utf-8')
                    body = ''.encode('utf-8')
                else:
                    # 파일 MIME 타입 결정
                    mime_type, _ = mimetypes.guess_type(path)
                    if mime_type is None:
                        mime_type = 'application/octet-stream'  # 기본 값으로 바이너리 데이터 설정

                    is_text_file = mime_type.startswith('text/')
                    
                    if is_text_file:
                        # 텍스트 파일은 utf-8로 읽고 인코딩
                        with open(path, 'r', encoding='utf-8') as f:
                            body = f.read().encode('utf-8')
                    else:
                        # 바이너리 파일은 그대로 읽기
                        with open(path, 'rb') as f:
                            body = f.read()

                    header = 'HTTP/1.1 200 OK\r\n'
                    header += 'Server: Our server\r\n'
                    header += 'Connection: close\r\n'
                    header += f'Content-Type: {mime_type}; charset=utf-8\r\n'
                    header += f'Content-Length: {len(body)}\r\n'
                    header += '\r\n'
                    header = header.encode('utf-8')

                response = header + body
                conn.sendall(response)
        except KeyboardInterrupt:
            print('Shutdown server')
            break
