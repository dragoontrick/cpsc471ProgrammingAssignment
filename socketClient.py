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

print("connected to server")

# 
# Packet Structure:
#   1. First 4 bytes   = length of command, X
#   2. Next X bytes    = command
#   3. Next 10 bytes   = length of next data, Y
#   4. Next Y bytes    = data
# Repeat steps 3 and 4 if needed
# send all data at once through `datatransfer.sendData(sock, packet)`
# 
isConnected = True
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
        if len(userInput) < 2 or userInput[1] == "":
            fileName = input("ftp > Enter File Name: ")
        else:
            fileName = userInput[1]
        
        fileNamelenStr = datatransfer.prepareSize(len(fileName))
        # send fileName
        # sends: "0003get0000000008file.txt"
        print("Getting " + fileName + " from server")
        datatransfer.sendData(clientSocket, commandLenStr + command + fileNamelenStr + fileName)

        fileDataLength = int(datatransfer.recvData(clientSocket, 10).decode())
        fileData = datatransfer.recvData(clientSocket, fileDataLength).decode()
        # print(file)
        if fileData == "FAILURE":
            print("ERROR file not found on server")
            print("Try command `ls` to see list of files on server")
            continue

        filePath = "clientfiles/" + fileName
        print("Saving the file data to `" + filePath + "`")
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
        datatransfer.sendData(clientSocket, commandLenStr + command)

        fileNamesLength = int(datatransfer.recvData(clientSocket, 10).decode())
        fileNames = datatransfer.recvData(clientSocket, fileNamesLength).decode()
        print("Files in Server:")
        fileNames = fileNames.split(' ')
        for file in fileNames:
            print("   -", file)

    elif command == "put":
        #filename = 'clientfiles/put.txt'
        fileName = ""
        if len(userInput) < 2 or userInput[1] == "":
            fileName = input("ftp > Enter File Name: ")
        else:
            fileName = userInput[1]

        fileNamelenStr = datatransfer.prepareSize(len(fileName))
            # send fileName
            # sends: "0003get0000000008file.txt"
        print("putting " + fileName + " to server")
        

        fileNameLength = len(fileName) #added
        fi = open("clientfiles/"+ fileName, "r") 
        
        dataT = fi.read()

        datatransfer.sendData(clientSocket, commandLenStr + command + fileNamelenStr + fileName + dataT)
        fi.close() #end of previous

            # print(file)

# Close the socket
clientSocket.close()
