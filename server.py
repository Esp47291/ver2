import socket

def read_html_file(filename):
    # Читаем файл из текущей папки (без templates/)
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()

def handle_request(client_socket):
    try:
        request = client_socket.recv(1024).decode('utf-8')
        print("Получен запрос:\n", request)

        # Обрабатываем только GET-запросы (по условию)
        if request.startswith("GET"):
            # Возвращаем contacts.html
            html_content = read_html_file('contacts.html')

            response = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/html; charset=utf-8\r\n"
                f"Content-Length: {len(html_content)}\r\n"
                "Connection: close\r\n"
                "\r\n"
                + html_content
            )
        else:
            # Для других методов — ошибка или заглушка
            response = (
                "HTTP/1.1 405 Method Not Allowed\r\n"
                "Content-Length: 0\r\n"
                "Connection: close\r\n"
                "\r\n"
            )

        client_socket.sendall(response.encode('utf-8'))
    except FileNotFoundError:
        # Если файл не найден
        error_page = "<h1>404: Файл contacts.html не найден</h1>"
        response = (
            "HTTP/1.1 404 Not Found\r\n"
            "Content-Type: text/html; charset=utf-8\r\n"
            f"Content-Length: {len(error_page)}\r\n"
            "Connection: close\r\n"
            "\r\n"
            + error_page
        )
        client_socket.sendall(response.encode('utf-8'))
    except Exception as e:
        # Любая другая ошибка
        print(f"Ошибка: {e}")
        error_page = "<h1>500: Внутренняя ошибка сервера</h1>"
        response = (
            "HTTP/1.1 500 Internal Server Error\r\n"
            "Content-Type: text/html; charset=utf-8\r\n"
            f"Content-Length: {len(error_page)}\r\n"
            "Connection: close\r\n"
            "\r\n"
            + error_page
        )
        client_socket.sendall(response.encode('utf-8'))
    finally:
        client_socket.close()

def start_server(host='localhost', port=8080):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"✅ Сервер запущен на http://{host}:{port}")

    try:
        while True:
            client_socket, addr = server_socket.accept()
            print(f"🌐 Подключение от {addr}")
            handle_request(client_socket)
    except KeyboardInterrupt:
        print("\n🛑 Сервер остановлен.")
    finally:
        server_socket.close()

if __name__ == '__main__':
    start_server()