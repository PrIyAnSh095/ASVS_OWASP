import socket
import threading

HOST = '0.0.0.0'
PORT = 8000
BUFFER_SIZE = 4096


def recv_until(sock, delimiter: bytes, buffer: bytes) -> tuple[bytes, bytes]:
    while delimiter not in buffer:
        chunk = sock.recv(BUFFER_SIZE)
        if not chunk:
            raise ConnectionError('Client disconnected before headers completed')
        buffer += chunk
    index = buffer.index(delimiter)
    return buffer[:index], buffer[index + len(delimiter):]


def parse_headers(header_block: bytes) -> dict:
    lines = header_block.decode('iso-8859-1').split('\r\n')
    headers = {}
    for line in lines[1:]:
        if ':' in line:
            name, value = line.split(':', 1)
            headers[name.strip().lower()] = value.strip()
    return headers


def read_exact(buffer: bytes, sock: socket.socket, length: int) -> tuple[bytes, bytes]:
    while len(buffer) < length:
        chunk = sock.recv(BUFFER_SIZE)
        if not chunk:
            raise ConnectionError('Client disconnected before full body arrived')
        buffer += chunk
    return buffer[:length], buffer[length:]


def read_chunked_body(buffer: bytes, sock: socket.socket) -> tuple[bytes, bytes]:
    body = b''
    while True:
        while b'\r\n' not in buffer:
            chunk = sock.recv(BUFFER_SIZE)
            if not chunk:
                raise ConnectionError('Client disconnected while reading chunk size')
            buffer += chunk

        line, buffer = buffer.split(b'\r\n', 1)
        chunk_size = int(line.split(b';', 1)[0].strip(), 16)

        if chunk_size == 0:
            while len(buffer) < 2:
                chunk = sock.recv(BUFFER_SIZE)
                if not chunk:
                    raise ConnectionError('Client disconnected during chunk terminator')
                buffer += chunk
            if not buffer.startswith(b'\r\n'):
                raise ValueError('Malformed chunk terminator')
            buffer = buffer[2:]
            return body, buffer

        chunk_data, buffer = read_exact(buffer, sock, chunk_size + 2)
        if not chunk_data.endswith(b'\r\n'):
            raise ValueError('Chunk data missing terminating CRLF')
        body += chunk_data[:-2]


def build_response(content: str) -> bytes:
    body = content.encode('utf-8')
    headers = [
        'HTTP/1.1 200 OK',
        'Content-Type: text/plain; charset=utf-8',
        f'Content-Length: {len(body)}',
        'Connection: close',
        '',
        ''
    ]
    return '\r\n'.join(headers).encode('utf-8') + body


def select_backend_mode(path: str, headers: dict) -> str:
    has_te = 'transfer-encoding' in headers
    has_cl = 'content-length' in headers
    if path.startswith('/clte'):
        return 'te' if has_te else ('cl' if has_cl else 'none')
    if path.startswith('/tecl'):
        return 'cl' if has_cl else ('te' if has_te else 'none')
    return 'te' if has_te else ('cl' if has_cl else 'none')


def parse_request(sock: socket.socket, buffer: bytes) -> tuple[str, dict, bytes, str, str]:
    header_block, buffer = recv_until(sock, b'\r\n\r\n', buffer)
    request_line = header_block.decode('iso-8859-1').split('\r\n', 1)[0]
    headers = parse_headers(header_block)
    path = request_line.split(' ')[1] if ' ' in request_line else '/'
    mode = select_backend_mode(path, headers)

    if mode == 'te':
        body, buffer = read_chunked_body(buffer, sock)
    elif mode == 'cl':
        length = int(headers.get('content-length', '0'))
        body, buffer = read_exact(buffer, sock, length)
    else:
        body = b''

    return request_line, headers, buffer, body.decode('utf-8', errors='replace'), mode


def build_analysis_text(request_line: str, headers: dict, body: str, path: str, mode: str) -> str:
    transfer_encoding = headers.get('transfer-encoding', '')
    content_length = headers.get('content-length', '')
    return (
        f'backend-mode: {mode}\n'
        f'path: {path}\n'
        f'request-line: {request_line}\n'
        f'transfer-encoding: {transfer_encoding}\n'
        f'content-length: {content_length}\n'
        f'body-length: {len(body)}\n'
        f'body: {body}\n'
    )


def handle_client(client_sock: socket.socket, addr):
    client_sock.settimeout(10)
    buffer = b''
    try:
        while True:
            request_line, headers, buffer, body, mode = parse_request(client_sock, buffer)
            path = request_line.split(' ')[1] if ' ' in request_line else '/'
            response_text = build_analysis_text(request_line, headers, body, path, mode)
            client_sock.sendall(build_response(response_text))
            if not buffer:
                break
    except Exception as exc:
        client_sock.sendall(build_response(f'backend error: {exc}\n'))
    finally:
        client_sock.close()


def run_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.bind((HOST, PORT))
        server_sock.listen(5)
        print(f'Vulnerable backend listening on {HOST}:{PORT}')
        while True:
            client_sock, addr = server_sock.accept()
            threading.Thread(target=handle_client, args=(client_sock, addr), daemon=True).start()


if __name__ == '__main__':
    run_server()
