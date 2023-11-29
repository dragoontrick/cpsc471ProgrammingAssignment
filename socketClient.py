# Client code
import socket

import send_file

# Name and port number of the server to
# which want to connect .
# serverAddr = "csu.fullerton.edu" # only works with localhost?
serverAddr = "localhost"
serverPort = 1234 
# Create a socket
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect to the server
clientSocket.connect((serverAddr, serverPort))
print("connected to server")
# A string we want to send to the server
# data = "Hello world ! This is a very long string."
# # Send that string!
# clientSocket.send(data.encode())

isConnected = True

#
receivingData = False
#

while isConnected:
    cmd = input("ftp > ").split(' ')
    send_file.sendData(clientSocket, cmd[0])

    if cmd[0] == "quit":
        # send format: "quit"
        isConnected = False
        break
    elif cmd[0] == "get":
        # send format: "get <length of filename?> <FILENAME>"
        fileName = cmd[1]
        # send fileName
        send_file.sendData(clientSocket, fileName)
        print("ftp > Getting " + fileName + " from server")
    elif cmd[0] == "put":
        # send format: "put <length of filename?> <FILENAME> <length of file> <FILEDATA>"
        pass
    elif cmd[0] == "ls":
        # send format: "ls"
        receivingData = True ##
        pass    

    # print("Sent Data to server!")

    # Receiving data from the server
    #send_file.recvData()

    if receivingData == True:
        # TODO -> Need to fix the broken pipe error when running the ls command for a second time
        data = send_file.recvData(clientSocket, 1024)
        data_decoded = data.decode('utf-8')

        print(data_decoded)
        receivingData = False


print("Closing now...")

# Close the socket
clientSocket.close()
