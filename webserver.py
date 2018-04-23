## Aidan Payne
## IFT 520
## Python basic web server

import socket
import threading

class ThreadedWebServer(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))

	##	Main process: Listen for incoming traffic on predefined socket, spawn thread to handle
    def listen(self):
        self.socket.listen(5)
        print("Serving HTTP on port",self.port,". . .")
        while True:
            client, address = self.socket.accept()
            threading.Thread(target = self.listenToClient, args = (client, address)).start()
            ##self.listenToClient(client, address)

	##	Given file, determine appropriate MIME type for HTTP OK
    def contentType(self,filepath):
        extension = filepath[filepath.index('.'):]
        ##print("extension: ",extension)
        if extension == '.jpg' or extension == '.jpeg':
            contentType = 'image/jpeg'
        elif extension == '.gif':
            contentType = 'image/gif'
        elif extension == '.ico':
            contentType = 'image/vnd.microsoft.icon'
        elif extension == '.mp3':
            contentType = 'audio/mpeg'
        elif extension == '.mp4':
            contentType = 'video/mp4'
        return contentType

	##	Handler for client HTTP requests
    def listenToClient(self, client, address):
        ##print("Starting thread")
        size = 1024
        while True:
            try:
                data = client.recv(size)
                ##print(data.decode())
                if data:
                    request = data.decode()
                    request = request.split()
                    ##print("request: ",request)
                    if len(request[1]) > 1:
                        fileName = "."+request[1]
                        ##print(fileName)
                        ##print("request: ",request[1])
                        try:
                            content = open(fileName, 'br')
                        except FileNotFoundError:
                            response = """HTTP/1.0 404 Not Found\r\n\r\n<!DOCTYPE HTML><html><head><title>404 Not Found</title></head><body><h1>404 Resource Not Found</h1><img src="sadface.jpg"/></body></html>\r\n"""
                            client.sendall(response.encode())
                            client.close()
                        contentData = content.read()
                        fileType = self.contentType(request[1])
                        ##print(fileType)
                        header = 'HTTP/1.0 200 OK\r\nContent-Type: '+fileType+'\r\n\r\n'
                        header = header.encode('utf-8')
                        response = header + contentData
                        ##print(response)
                        client.sendall(response)
                        client.close()
                    else:
                        response = """HTTP/1.0 200 OK\r\n\r\n<!DOCTYPE HTML><html><head><title>Python WebServer</title></head><body><h1>Welcome to the landing page!</h1><audio controls><source src="08510.mp3" type="audio/mpeg"></audio><br><video width="480" height="480" controls><source src="paws.mp4" type="video/mp4"></video><br><img src="test.jpg"/><img src="test2.gif"/></body></html>\r\n"""
                        client.sendall(response.encode())
                        client.close()
                else:
                    raise error('Client disconnected')
            except:
                 client.close()
                 return False

if __name__ == "__main__":
    port = 8888
    ThreadedWebServer('',port).listen()
