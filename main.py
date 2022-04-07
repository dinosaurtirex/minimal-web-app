import socket 
from views import (index, blog)

URLS = {
    '/': index,
    '/blog': blog,
}


class WebApp:

    def __init__(self, urls):
        self.URLS = urls 

    def __generate_headers(self, method, url):
        if not method == 'GET':
            return ('HTTP/1.1 405 Method not allowed\n\n', 405)

        if url not in URLS:
            return ('HTTP/1.1 404 Not found\n\n', 404)

        return ('HTTP/1.1 200 OK\n\n', 200)

    def __parse_request(self, request):
        parsed = request.split(" ")
        return (parsed[0], parsed[1])

    def __generate_content(self, code, url):
        if code == 404:
            return '<h1>404</h1><p>Not found</p>'
        if code == 405:
            return '<h1>405</h1><p>Method not allowed</p>'  
        return self.URLS[url]()

    def __generate_response(self, request):
        method, url = self.__parse_request(request)
        headers, code = self.__generate_headers(method, url)
        body = self.__generate_content(code, url)
        return (headers + body).encode()

    def run(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(('localhost', 5000))
        server_socket.listen()
        while True:
            client_socket, address = server_socket.accept()
            request = client_socket.recv(1024).decode('utf-8')
            response = self.__generate_response(request)
            client_socket.sendall(response)
            client_socket.close()

if __name__ == '__main__':
    WebApp(URLS).run()