# سلام عزیزم چت روم شما بررسی شد.
# تشکر میکنم بابت این که تقریبا 
# اکثر مواردی که گفته شده انجام شده.
# مواردی که باید اصلاح بشه:
# 1. وقتی کاربر پیامی میفرسته باید کنار پیامش اسمش نوشته بشه 
# چون همه دارن میبینن و باید بدونن کدوم پیام برای کی هست.
# 2. زمان پیام ثبت میشه اما تو سرور نمایش داده میشه بهتره 
# این زمان رو تو کلاینت نمایش بدین چون نمایشش تو سرور بی فایده هست.
# 3. یکی درمیون موقع فرستادن پیام کلاینت اینطوری پیام رو ازمون میخواد
# Message:
# [تو بعدی اینو نمیگه و خالیه]
# بهتره هر سری message رو بگه.


import socket
import threading


HOST = "127.0.0.1"
PORT = 8080

clients = []
users = []

def receive_messages(conn, username):
        while True:
          try:
                message = conn.recv(1024).decode()
          except ConnectionResetError:
                message = ""

          if not message:
               if username in users:
                    users.remove(username)

               if conn in clients:
                    clients.remove(conn)

               leave_message = f"{username} left the chat"

               for client in clients:
                    client.send(leave_message.encode())
               break
          if message == "exit":
                users.remove(username)
#پیغام خروج
                leave_message = f"{username} left the chat"
#ارسال پیام برای همه کلاینت های موجود
                for client in clients:
                    client.send(leave_message.encode())
                clients.remove(conn)
                break
#انلاین بودن کاربر

          if message == "users":
                  online_users = ", ".join(users)
                  conn.send(online_users.encode())
                  continue
        
          print(message)
          for client in clients:
            client.send(message.encode())
#conn.close()

def handle_client(conn, addr):
    with conn:
        print("Connection from:", addr)
        clients.append(conn)

        username = conn.recv(1024).decode()
        print("Username:", username)
        users.append(username)

#گرفتن اسم ووردی جدید 
        join_message = f"{username} joined the chat"
        print(join_message)

        for client in clients:
            client.send(join_message.encode())
        receive_thread = threading.Thread(
            target=receive_messages,
            args=(conn, username)
        )

        receive_thread.start()
        receive_thread.join()

        conn.close()
 
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:

    server.bind((HOST, PORT))
    server.listen()

    print(f"Server is running on {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()

        thread = threading.Thread(
            target=handle_client,
            args=(conn, addr)
        )

        thread.start()