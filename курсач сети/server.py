from ast import While
from http import client
import socket


def start_my_server():
    # Создание именно серверного сокета (пока не задана адрес, сокет будет клиентский)
    # Создаём сокет для работы c Web
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # задаём сокету адрес и хост, в unix системах необходимо задавать порт больше 1024, чтобы небыло конфликтов
    server.bind(("127.0.0.1", 8000))

    # создание приема, заданного колличетсва, которые будут в очереди, если больше , то сброшены
    server.listen(5)
    print("Сервер запущен!)")
    while True:
        try:
           
            # http://127.0.0.1:8000/home.html

            # получение данных о подключившемся, если никто не подключённ программа дальше не идёт
            client_socket, address = server.accept()
            print("client_socket=",client_socket)
            print("address=",address)
            # получение данных от клиента(с заданым резмером), её нужно декодировать
            data = client_socket.recv(1024).decode("utf-8")
            # print(data)

            content = load_page(data)
            client_socket.send(content)  # отправка пользователю
            # дальнейшая передача данных будет запрещена
            client_socket.shutdown(socket.SHUT_WR)
        except KeyboardInterrupt:
            print("Сервер выключился...")


def load_page(request_data):
    # Заголовки для того, чтобы работало в любом браузере
    HDRS = "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n"
    HDRS_404 = "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n"
    # Получаем данные , которые запросил пользователь
    path = request_data.split(" ")[1]
    response = " "
    # открываем папку с данными и конкретную страницу, при помаще флага "rb" сразу в байтовом виде
    try:
        with open('pages'+path, "rb") as file:
            response = file.read()
        return HDRS.encode("utf-8")+response
    except FileNotFoundError:
        return(HDRS_404 + "Ой, такой страницы не существует!").encode("utf-8")

if __name__ == "__main__":
    start_my_server()
