# import libraries for server code
import socket
import datatransfer 

import os
import sys

# Command line checks
if len(sys.argv) < 2:
    print("USEAGE: python3 server.py <PORT NUMBER>")
    sys.exit(1)

# Getting the port on which to listen
#serverPort = 1234
serverPort = int(sys.argv[1])

# Create a TCP socket
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

# Bind the socket to the port
serverSocket.bind(("", serverPort))
# Start listening for incoming connections
serverSocket.listen(1)  # This number refers to the number of acceptable connections

print("The server is ready to receive")

# Forever accept incoming connections
while True:
    print("[WAIT] For connections...")
    # Accept a connection; get client’s socket
    connectionSocket, addr = serverSocket.accept()
    print("[CONNECTED] to client:", addr)
    # Keep the connection with client alive until server recieves `quit` command
    connected = True
    while connected:
        print("[WAIT] For command from client...")
        commandLength = int(datatransfer.recvData(connectionSocket, 4).decode())
        command = datatransfer.recvData(connectionSocket, commandLength).decode()
        print("[INFO] Recieved command:", command)

        succesful = True

        if command == "quit":
            connected = False
            break  # breaks out of `while connected: ` loop
        elif command == "get":
            fileNameLength = int(datatransfer.recvData(connectionSocket, 10).decode())
            fileName = datatransfer.recvData(connectionSocket, fileNameLength).decode()
            print("[INFO] Recieved file name:", fileName)

            if datatransfer.sendFile(connectionSocket, "serverfiles/" + fileName) < 0:
                succesful = False

        elif command == "put":
            fileNameLength = int(datatransfer.recvData(connectionSocket, 10).decode())
            filename = datatransfer.recvData(connectionSocket, fileNameLength).decode()

            fileDataLength = int(datatransfer.recvData(connectionSocket, 10).decode())
            fileData = datatransfer.recvData(connectionSocket, fileDataLength).decode()    #
            

            filePath = "serverfiles/" + filename
            try:
            # tries to create a file if it DOES NOT exists
            

                fo = open(filePath, 'x')
                fo.write(fileData)
                fo.close()
            except FileExistsError:
            # simply opens the file because it DOES exists 
                fo = open(filePath, 'w')
                fo.write(fileData)
                fo.close()



        elif command == "ls":
            filenames = os.listdir('serverfiles')
            print("[INFO]", filenames)

            # TODO: might break for filenames with spaces: `file hello.txt`
            filenames_string = ' '.join(filenames)

            fileNamesLength = datatransfer.prepareSize(len(filenames_string))

            datatransfer.sendData(connectionSocket, fileNamesLength + filenames_string)
        
        if succesful:
            print("[SUCCESS] Executed:", command)
        else:
            print("[FAILURE] Tried to execute:", command)
    
    print("[DISCONNECTED] From client:", addr)
    # Close the socket
    connectionSocket.close()
