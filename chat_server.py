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

# Configure logging
import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

server_port = 12000

clients = []


def connection_handler(connection_socket, address):
  # Read data from the new connectio socket
  #  Note: if no data has been sent this blocks until there is data

  # Meg - For Extra Credit
  # Receive chosen username
  # username_encoded = connection_socket.recv(1024)

  # Decode Username
  # username = username_encoded.decode()
  
  # Meg - Keep track of connected clients
  # clients[username] = connection_socket
  
  # Log query information
  # log.info("Received query test \"" + str(username) + "\"")
  
  # Perform some server operations on data to generate response
  # time.sleep(5)
  # response = "Your username is: " + username.upper()
  
  # Sent response over the network, encoding to UTF-8
  # connection_socket.send(response.encode())
  
    while True:
        message_encoded = connection_socket.recv(1024)
        if not message_encoded:
            break
        message = message_encoded.decode()
        log.info("Received query test \"" + str(message) + "\"")
        time.sleep(5)
        response = message.upper()
        # connection_socket.send(response.encode())

        # Brandon - send message to other client (this version only works with hard coded numbers (two clients))
        # ***address is the client_counter in main***
        if address == 0:
           clients[1].send(response.encode())
        else:
           clients[0].send(response.encode())
        

    # Close client socket
    # print(clients)
    # del clients[connection_socket]
    connection_socket.close()
    # print(clients)

  

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

      # Meg - Start a new thread
      # Brandon - made temporary change to second args (originally "address")
      client_thread = threading.Thread(target=connection_handler, args=(connection_socket, client_counter))
      client_thread.start()
      log.info("Connected to client at " + str(address))

      # Brandon - temporary way to identify sockets to use for forwarding messages
      clients.insert(client_counter, connection_socket)
      client_counter +=1
      
      # Pass the new socket and address off to a connection handler function
      # connection_handler(connection_socket, address)
  finally:
    server_socket.close()


if __name__ == "__main__":
  main()
