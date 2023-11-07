# Client code
from socket import *

# Name and port number of the server to
# which want to connect .
serverName = "ecs.fullerton.edu"
serverPort = 12000 
# Create a socket
clientSocket = socket(AF_INET, socket.SOCKSTREAM)
# Connect to the server
clientSocket.connect (( serverName , serverPort ))
# A string we want to send to the server
data = "Hello world ! This is a very long string."
# Send that string!
clientSocket.send(data)

# Close the socket
clientSocket.close()
