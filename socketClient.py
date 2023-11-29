# Client code
import socket
import datatransfer

import sys

# Command line checks
if len(sys.argv) < 3:
    print("USEAGE: python3 socketClient.py <server machine> <server port>")
    sys.exit(1)

# Getting port number and the name of the server we want to connect to
serverAddr = sys.argv[1]
serverPort = int(sys.argv[2])

# Name and port number of the server to
# which want to connect .
# serverAddr = "csu.fullerton.edu" # only works with localhost?
#serverAddr = "localhost"

# Create a socket
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Try connecting to the server on the port specified by the client
    clientSocket.connect((serverAddr, serverPort))
    #isConnected = True
except ConnectionRefusedError:
    print(f"Could not connect to {serverAddr}:{serverPort}. The server may not be currently running or the port is wrong.")
    #isConnected = False
    sys.exit(1)

# Connect to the server
#clientSocket.connect((serverAddr, serverPort))

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
    userInput = input("ftp > ").split(' ')
    command = userInput[0]
    commandLenStr = datatransfer.prepareSize(len(command), 4)

    if command == "quit":
        # send format: "quit"
        isConnected = False
        datatransfer.sendData(clientSocket, commandLenStr + command)
        break
    elif command == "get":
        fileName = ""
        if len(userInput) < 2:
            fileName = input("ftp > Enter File Name: ")
        else:
            fileName = userInput[1]
        
        fileNamelenStr = datatransfer.prepareSize(len(fileName))
        # send fileName
        # we have to send all data at once
        # sends: "0003get0000000008file.txt"
        print("    Getting " + fileName + " from server")
        datatransfer.sendData(clientSocket, commandLenStr + command + fileNamelenStr + fileName)

        fileDataLength = int(datatransfer.recvData(clientSocket, 10).decode())
        fileData = datatransfer.recvData(clientSocket, fileDataLength).decode()
        # print(file)
        if fileData == "FAILURE":
            print("    ERROR file not found on server")
            continue

        filePath = "clientfiles/" + fileName
        print("    Saving the file data to `" + filePath + "`")
        try:
            # tries to create a file if it DOES NOT exists
            with open(filePath, 'x') as file:
                file.write(fileData)
        except FileExistsError:
            # simply opens the file because it DOES exists 
            with open(filePath, 'w') as file:
                file.write(fileData)

        print(f"    Data transfer complete! Filename: {fileName}, Bytes Transferred: {fileDataLength}")
        #print(f"    Filename: {fileName}")
        #print(f"    Bytes Transferred: {fileDataLength}")
        
    elif command == "ls":
        # send format: "ls"
        # receivingData = True ##
        datatransfer.sendData(clientSocket, commandLenStr + command)

        fileNamesLength = int(datatransfer.recvData(clientSocket, 10).decode())
        fileNames = datatransfer.recvData(clientSocket, fileNamesLength).decode()
        print("    Files in Server:")
        fileNames = fileNames.split(' ')
        for file in fileNames:
            print("    -", file)

    elif command == "put":
        pass


    # Receiving data from the server
    #datatransfer.recvData()

    # if receivingData == True:
    #     # TODO -> Need to fix the broken pipe error when running the ls command for a second time
    #     data = datatransfer.recvData(clientSocket, 1024)
    #     data_decoded = data.decode('utf-8')

    #     print(data_decoded)
    #     receivingData = False

# Close the socket
clientSocket.close()
