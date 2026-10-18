import socket
import threading
import time

HOST = "127.0.0.1"
PORT = 8080


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:

    client.connect((HOST, PORT))

    print("Connected to server!")

    username = input("Enter your username: ")
    client.send(username.encode())

    def receive_messages():
      while True:
        try:
           message = client.recv(1024).decode()

           if not message:
             break
        
           print(message)

        except OSError:
         break
      
    receive_thread = threading.Thread(
    target=receive_messages
)
    receive_thread.start()

    while True:
        
        message = input("Message: ")

        if message == "exit":
            client.send(message.encode())
            break
        

        current_time =time.strftime("%H:%M:%S")
        
        client.send(f"[{current_time}] {username}:{message}".encode())
