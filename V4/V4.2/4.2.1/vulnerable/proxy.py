import os
import socket
import threading

HOST = '0.0.0.0'
PORT = 5001
BACKEND_HOST = os.environ.get('BACKEND_HOST', 'backend')
BACKEND_PORT = int(os.environ.get('BACKEND_PORT', '8000'))
BUFFER_SIZE = 4096


def build_error_response(message: str, code: int = 400) -> bytes:
    body = f"{message}\n".encode('utf-8')
    headers = [
        f"HTTP/1.1 {code} {'Bad Request' if code == 400 else 'Error'}",
        'Content-Type: text/plain; charset=utf-8',
        f'Content-Length: {len(body)}',
        'Connection: close',
        '',
        ''
    ]
    return '\r\n'.join(headers).encode('utf-8') + body


def recv_until(sock, delimiter: bytes, buffer: bytes) -> tuple[bytes, bytes]:
    while delimiter not in buffer:
        chunk = sock.recv(BUFFER_SIZE)
        if not chunk:
            raise ConnectionError('Client disconnected while reading headers')
        buffer += chunk
    index = buffer.index(delimiter)
    return buffer[:index], buffer[index + len(delimiter):]


def parse_headers(header_block: bytes) -> dict:
    lines = header_block.decode('iso-8859-1').split('\r\n')
    headers = {}
    for line in lines[1:]:
        if ':' not in line:
            continue
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
    raw_body = b''
    while True:
        while b'\r\n' not in buffer:
            chunk = sock.recv(BUFFER_SIZE)
            if not chunk:
                raise ConnectionError('Client disconnected while reading chunk size')
            buffer += chunk

        length_line, buffer = buffer.split(b'\r\n', 1)
        raw_body += length_line + b'\r\n'
        chunk_size = int(length_line.split(b';', 1)[0].strip(), 16)

        if chunk_size == 0:
            while len(buffer) < 2:
                chunk = sock.recv(BUFFER_SIZE)
                if not chunk:
                    raise ConnectionError('Client disconnected during chunk terminator')
                buffer += chunk
            if not buffer.startswith(b'\r\n'):
                raise ValueError('Malformed chunk terminator')
            raw_body += b'\r\n'
            buffer = buffer[2:]
            return raw_body, buffer

        chunk_data, buffer = read_exact(buffer, sock, chunk_size + 2)
        if not chunk_data.endswith(b'\r\n'):
            raise ValueError('Chunk data missing terminating CRLF')
        raw_body += chunk_data


class RequestParseError(Exception):
    pass


def select_vulnerable_mode(path: str, headers: dict) -> str:
    has_te = 'transfer-encoding' in headers
    has_cl = 'content-length' in headers
    if path.startswith('/clte'):
        return 'cl' if has_cl else ('te' if has_te else 'none')
    if path.startswith('/tecl'):
        return 'te' if has_te else ('cl' if has_cl else 'none')
    return 'cl' if has_cl else ('te' if has_te else 'none')


def read_request(sock: socket.socket, buffer: bytes) -> tuple[bytes, dict, str, bytes]:
    header_block, buffer = recv_until(sock, b'\r\n\r\n', buffer)
    raw_headers = header_block + b'\r\n\r\n'
    request_line = header_block.decode('iso-8859-1').split('\r\n', 1)[0]
    path = request_line.split(' ')[1] if ' ' in request_line else '/'
    headers = parse_headers(header_block)
    raw_body = b''

    mode = select_vulnerable_mode(path, headers)
    if mode == 'te':
        raw_body, buffer = read_chunked_body(buffer, sock)
    elif mode == 'cl':
        length = int(headers['content-length']) if 'content-length' in headers else 0
        raw_body, buffer = read_exact(buffer, sock, length)

    return raw_headers + raw_body, headers, path, buffer


def forward_to_backend(raw_request: bytes) -> bytes:
    with socket.create_connection((BACKEND_HOST, BACKEND_PORT), timeout=5) as backend:
        backend.sendall(raw_request)
        backend.shutdown(socket.SHUT_WR)
        response_data = b''
        while True:
            chunk = backend.recv(BUFFER_SIZE)
            if not chunk:
                break
            response_data += chunk
    return response_data


def handle_client(client_sock: socket.socket, client_address):
    client_sock.settimeout(10)
    buffer = b''
    try:
        while True:
            raw_request, headers, path, buffer = read_request(client_sock, buffer)
            response = forward_to_backend(raw_request)
            client_sock.sendall(response)
            if not buffer:
                break
    except Exception as exc:
        client_sock.sendall(build_error_response(f'Proxy error: {exc}', 502))
    finally:
        client_sock.close()


def run_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.bind((HOST, PORT))
        server_sock.listen(5)
        print(f'Vulnerable proxy listening on {HOST}:{PORT}')
        while True:
            client_sock, client_address = server_sock.accept()
            threading.Thread(target=handle_client, args=(client_sock, client_address), daemon=True).start()


if __name__ == '__main__':
    run_server()
