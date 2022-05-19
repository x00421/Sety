from http import client
import socket


def start_my_server():
    # Создание именно серверного сокета (пока не задана адрес, сокет будет клиентский)
    # Создаём сокет для работы c Web
    # AF_INET- это семейство – IPv4Данный протокол использует IP размером в 32 бита, т.е. размером всего в 4 байта. Структурой он представляет — четыре числа в десятичном формате от 0 до 255 разделенных точками. В каждом таком числе 1 байт или 8 бит.
    # SOCK_STREAM - обеспечивает надежный двусторонний обмен потоками байтов, основанный на установлении соединения.
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   
    server.bind(("127.0.0.1", 80))

    # создание приема, заданного колличетсва, которые будут в очереди, если больше , то сброшены
    server.listen(5)
    print("Сервер запущен!)")
    while True:

        # http://127.0.0.1

        # получение данных о подключившемся, если никто не подключённ программа дальше не идёт
        client_socket, address = server.accept()
        #print("client_socket=", client_socket)
        #print("address=", address)
        # получение данных от клиента(с заданым резмером), её нужно декодировать
        data = client_socket.recv(1024).decode("utf-8")
        #print(data)

        content = load_page(data)

        client_socket.send(content)  # отправка пользователю
        # дальнейшая передача данных будет запрещена
        client_socket.shutdown(socket.SHUT_WR)

    print("Сервер выключился...")


def load_page(request_data):
    # Заголовки для того, чтобы работало в любом браузере
    HDRS = "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n"
    HDRS_404 = "HTTP/1.1 404 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n"
    # Получаем данные , которые запросил пользователь
    path = request_data.split(" ")[1]
    # print(path)
    response = " "
    if path == "/":
        with open('pages'+"/home.html", "rb") as file:
            response = file.read()
            return HDRS.encode("utf-8")+response
    else:
        # Проверка ответа сервера
        try:
            # открываем папку с данными и конкретную страницу, при помаще флага "rb" сразу в байтовом виде
            with open('pages'+path, "rb") as file:
                response = file.read()
            return HDRS.encode("utf-8")+response
        except FileNotFoundError:
            with open('pages'+"/404.html", "rb") as file:
                response = file.read()
            return HDRS_404.encode("utf-8")+response


if __name__ == "__main__":
    start_my_server()
