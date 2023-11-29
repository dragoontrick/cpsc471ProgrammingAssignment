# import libraries for server code
import socket
import send_file 

#
import os
import pickle
#

# The port on which to listen
serverPort = 1234

# Create a TCP socket
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
# Bind the socket to the port
serverSocket.bind(("", serverPort))
# Start liste ning for incoming connections
serverSocket.listen(1)  # This number refers to the number of acceptable connections

print("The server is ready to receive")

# The buffer to store the received data
data = ""

# Forever accept incoming connections
while True:
    print("\nWaiting for connections...")
    # Accept a connection; get client’s socket
    connectionSocket, addr = serverSocket.accept()
    print("Accepted connection from client: ", addr)
    connected = True
    while connected:
        print("    Waiting for command from client...")
        commandLength = int(send_file.recvData(connectionSocket, 4).decode())
        command = send_file.recvData(connectionSocket, commandLength).decode()
        print("    [INFO] Recieved command:", command)

        succesful = True

        if command == "quit":
            connected = False
            print("    [INFO] Closing connection with client:", addr)
            break  # breaks out of `while connected: ` loop
        elif command == "get":
            fileNameLength = int(send_file.recvData(connectionSocket, 10).decode())
            fileName = send_file.recvData(connectionSocket, fileNameLength).decode()
            print("    [INFO] Recieved file name:", fileName)

            if send_file.sendFile(connectionSocket, "serverfiles/" + fileName) < 0:
                succesful = False

        elif command == "ls":
            filenames = os.listdir('serverfiles')
            print("    [INFO]", filenames)

            # TODO: might break for this `file hello.txt`
            filenames_string = ' '.join(filenames)

            fileNamesLength = send_file.prepareSize(len(filenames_string))

            send_file.sendData(connectionSocket, fileNamesLength + filenames_string)
        
        if succesful:
            print("    [SUCCESS] Executed:", command)
        else:
            print("    [FAILURE] Tried to execute:", command)

    # Close the socket
    connectionSocket.close()
