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



def connection_handler(connection_socket, address):

    message = "You are connected to the server. "
    if connection_socket == connected_clients["Client X"]:
        message = message + "Welcome, Client X! Type a message and press 'enter' to send."
        connected_clients["Client X"].send(message.encode())
    else:
        if len(connected_clients) > 1:
            message = message + "Welcome, Client Y! Type a message and press 'enter' to send."
            connected_clients["Client Y"].send(message.encode())
 
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
                # If the message is 'bye'
                if response == "bye":
                    # Exit message received from Client X
                    if (connection_socket == connected_clients["Client X"]):
                        response = "Client X has left the chat"
                        print(response)
                        # Tell Client Y that Client X left
                        connected_clients["Client Y"].send(response.encode())
                        server_active = False # boolean to close outer loop
                    # Exit message received from Client Y
                    if (connection_socket == connected_clients["Client Y"]):
                        response = "Client Y has left the chat"
                        print(response)
                        # Tell Client X that Client Y left
                        connected_clients["Client X"].send(response.encode())
                        server_active = False # boolean to close outer loop


                # Brandon - send message to other client (this version only works with hard coded numbers (two clients))
                # ***address is the client_counter in main***
                # Meg - Adjusted to use usernames
                else:
                    log.info("Received query test \"" + str(message) + "\"")
#                   time.sleep(2)
                    # Message received from Client X
                    if connection_socket == connected_clients["Client X"]:
                        response = "Client X: " + response;
                        # Send message to Client Y
                        connected_clients["Client Y"].send(response.encode())
                    # Message received from Client Y
                    else:
                        response = "Client Y: " + response;
                        # Send message to Client X
                        connected_clients["Client X"].send(response.encode())
            except:
                print("There is an error")
            
            # If a client exited, break the loop
            if server_active == False:
                break
        if server_active == False:
            break

    # Close client socket
    if connection_socket == connected_clients["Client X"]:
        del connected_clients["Client X"]
    if connection_socket == connected_clients["Client Y"]:
        del connected_clients["Client Y"]
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

      # Meg - Keep track of connected_clients with username:
      if len(connected_clients) == 0:
          connected_clients["Client X"] = connection_socket
      else:
          connected_clients["Client Y"] = connection_socket

      inputs.append(connection_socket)
      outputs.append(connection_socket)
      # for key, value in connected_clients.items():
          # print(key, value)


      # Meg - Start a new thread
      # Brandon - made temporary change to second args (originally "address")
      client_thread = threading.Thread(target=connection_handler, args=(connection_socket, client_counter))
      client_thread.start()
      log.info("Connected to client at " + str(address))

      # Brandon - temporary way to identify sockets to use for forwarding messages
      clients.insert(client_counter, connection_socket)
      client_counter +=1

  finally:
    server_socket.close()


if __name__ == "__main__":
  main()
