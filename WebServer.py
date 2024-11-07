from socket import *
import sys
import os

serverSocket = socket(AF_INET, SOCK_STREAM)
serverPort = 6788
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

print("Ready to serve...")

while True:
    connectionSocket, addr = serverSocket.accept()
    
    try:
        message = connectionSocket.recv(1024).decode()
        
        filename = message.split()[1]
        
        if filename == "/":
            filename = "/index.html"

        filepath = filename[1:]
        
        if os.path.isfile(filepath):
            with open(filepath, "rb") as f:
                outputdata = f.read()

            connectionSocket.send("HTTP/1.1 200 OK\r\n".encode())
            connectionSocket.send("Content-Type: text/html\r\n\r\n".encode())
            connectionSocket.sendall(outputdata)
    except Exception as e:
        connectionSocket.send("HTTP/1.1 404 Not Found\r\n".encode())
        connectionSocket.send("Content-Type: text/html\r\n\r\n".encode())
        connectionSocket.send("<html><head></head><body><h1>404 Not Found</h1></body></html>".encode())
        print(e)
    
    connectionSocket.close()

serverSocket.close()
sys.exit()
