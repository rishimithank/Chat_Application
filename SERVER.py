import socket
import threading

HOST = '192.168.43.65'
PORT = 1234 
active_clients = [] 


def listening_for_messages(client, username):

    while 1:

        message = client.recv(2048).decode('utf-8')
        if message != '':
            
            final_msg = username + '~' + message
            sending_messages_to_all_clients(final_msg)

        else:
            print(f"The message send from client {username} is empty")



def sending_message_to_clients(client, message):

    client.sendall(message.encode())



def sending_messages_to_all_clients(message):
    
    for user in active_clients:

        sending_message_to_clients(user[1], message)


def client_handler(client):
    
    
    
    while 1:

        username = client.recv(2048).decode('utf-8')
        if username != '':
            active_clients.append((username, client))
            prompt_message = "SERVER~" + f"{username} added to the chat"
            sending_messages_to_all_clients(prompt_message)
            break
        else:
            print("Client username is empty")

    threading.Thread(target=listening_for_messages, args=(client, username, )).start()


def main():

    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
          
        server.bind((HOST, PORT))
        print(f"Running the server on {HOST} and {PORT}")
    except:
        print(f"Unable to bind to host {HOST} and port {PORT}")

    
    server.listen()

    
    while 1:

        client, address = server.accept()
        print(f"Successfully connected to client {address[0]} {address[1]}")

        threading.Thread(target=client_handler, args=(client, )).start()


if __name__ == '__main__':
    main()
