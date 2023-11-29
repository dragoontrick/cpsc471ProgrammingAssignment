# Client code
import socket

import datatransfer

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
