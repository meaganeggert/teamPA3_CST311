#!env python

"""Chat server for CST311 Programming Assignment 3"""
__author__ = "Team 5"
__credits__ = [
        "Meagan Eggert",
        "Maria Imperatrice",
        "Brandon Hoppens",
        "Ryan Matsuo"
]


import socket as s
import time
import threading
import select
import sys

# Configure logging
import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

server_port = 12000

clients = []
connected_clients = {}

inputs = []
outputs = []

offline_messages = []

def connection_handler(connection_socket, address):

    # Maria - Username specification and offline messages
    # Initial prompt, stores connection with username
    connection_socket.send("Welcome to the chat! Please enter your username: ".encode())
    username = connection_socket.recv(1024).decode().strip()
    connected_clients[username] = connection_socket

    # Sends offline message to connected user and formats
    for i, msg in enumerate(offline_messages):
        connection_socket.send(msg.encode())
        if i < len(offline_messages) - 1:
            connection_socket.send("\n".encode())

    offline_messages.clear()

    server_active = True

    while server_active:
        try:
            input_ready, output_ready, err = select.select(inputs, outputs, [])
        except:
            print("Meagan broke something in the server code")
            break

        # Meg - For each "ready" possible input, i.e. Client X or Client Y
        for input in input_ready:
            try:
                # If there's a message, receive it
                message_encoded = connection_socket.recv(1024)
                if not message_encoded:
                    break
                message = message_encoded.decode()
                response = message.lower()
                # Maria - If the message is 'bye' - for username
                if response == "bye":
                    exit_message = username + " has left the chat."
                    for user, sock in connected_clients.items():
                        if sock != connection_socket:
                            sock.send(exit_message.encode())
                    server_active = False

                # Brandon - send message to other client (this version only works with hard coded numbers (two clients))
                # ***address is the client_counter in main***
                # Maria - Adjusted for usernames
                else:
                    full_message = username + ": " + message
                    # Send message to other user
                    for user, sock in connected_clients.items():
                        if sock != connection_socket:
                            sock.send(full_message.encode())
                    # If the other user is not connected, store the message
                        if len(connected_clients) < 2:
                            offline_messages.append(full_message)
                                
            except:
                print("There is an error")
            
            # If a client exited, break the loop
            if server_active == False:
                break
        if server_active == False:
            break

    if not server_active:
        if username in connected_clients and connected_clients[username] == connection_socket:
            del connected_clients[username]
            inputs.remove(connection_socket)
            outputs.remove(connection_socket)

    connection_socket.close()
    # for key, value in connected_clients.items():
        # print(key, value)
  

def main():
  # Create a TCP socket
  # Notice the use of SOCK_STREAM for TCP packets
  server_socket = s.socket(s.AF_INET,s.SOCK_STREAM)
  
  # Assign port number to socket, and bind to chosen port
  server_socket.bind(('',server_port))
  
  # Configure how many requests can be queued on the server at once
  server_socket.listen(1)
  
  # Alert user we are now online
  log.info("The server is ready to receive on port " + str(server_port))

  # Brandon - Temporary counter used to identify sockets via the clients array.
  client_counter = 0
  
  # Surround with a try-finally to ensure we clean up the socket after we're done
  try:
    # Enter forever loop to listen for requests
    while True:
      # When a client connects, create a new socket and record their address
      connection_socket, address = server_socket.accept()

      inputs.append(connection_socket)
      outputs.append(connection_socket)
      # for key, value in connected_clients.items():
          # print(key, value)


      # Meg - Start a new thread
      # Brandon - made temporary change to second args (originally "address")
      client_thread = threading.Thread(target=connection_handler, args=(connection_socket, client_counter))
      client_thread.start()
      log.info("Connected to client at " + str(address))


  finally:
    server_socket.close()


if __name__ == "__main__":
  main()
