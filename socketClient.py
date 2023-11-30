# Client code
import socket
import datatransfer

serverAddr = "localhost"
serverPort = 1234 
# Create a socket
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect to the server
# print(socket.gethostbyname(serverAddr))
clientSocket.connect((serverAddr, serverPort))
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
        pass

# Close the socket
clientSocket.close()
