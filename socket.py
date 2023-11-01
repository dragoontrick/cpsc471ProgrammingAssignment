
#import libraries for server code
import socket

# The port on which to listen
serverPort = 12000

# Create a TCP socket
serverSocket = socket (AF INET ,SOCK STREAM) 
# Bind the socket to the port
serverSocket.bind (( '' , serverPort )) 
# Start liste ning for incoming connections
serverSocket.listen(1)  #This number refers to the number of acceptable connections

print”The server is ready to receive”

# The buffer to store the received data
data = ""

 # Forever accept incoming connections
while 1 :
 # Accept a connection; get client’s socket
connectionSocket,addr = serverSocket.accept () 

 # Receive whatever the newly connected client has to send
data = connectionSocket.recv(40)
print data


 # Close the socket
connection Socket.close()
