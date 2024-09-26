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

clients = {}


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
        connection_socket.send(response.encode())
        

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
  
  # Surround with a try-finally to ensure we clean up the socket after we're done
  try:
    # Enter forever loop to listen for requests
    while True:
      # When a client connects, create a new socket and record their address
      connection_socket, address = server_socket.accept()

      # Meg - Start a new thread
      client_thread = threading.Thread(target=connection_handler, args=(connection_socket, address))
      client_thread.start()
      log.info("Connected to client at " + str(address))
      
      # Pass the new socket and address off to a connection handler function
      # connection_handler(connection_socket, address)
  finally:
    server_socket.close()


if __name__ == "__main__":
  main()
