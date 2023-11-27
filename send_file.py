import socket

#def sendFileNames(sock: socket.socket, data: list):
#    numSent = 0
#    # Send the data!
#    while len(data) > numSent:
#        numSent += sock.send(data.encode())


def sendData(sock: socket.socket, data: str):
    numSent = 0
    # Send the data!
    while len(data) > numSent:
        numSent += sock.send(data.encode())

def sendFile(sock: socket.socket, fileName: str):
    fileInput = open(fileName, 'r')
    fileData = fileInput.read(65536)

    if fileData:
        dataSizeStr = str(len(fileData))

        # Prepend 0's to the size string
        # until the size is 10 bytes
        while len(dataSizeStr) < 10:
            dataSizeStr = "0" + dataSizeStr
        
        sendData(sock, dataSizeStr)

        # Prepend the size of the data to the
        # file data.
        # fileData = dataSizeStr + fileData	
        sendData(sock, fileData)


def recvData(sock: socket.socket, length: int):
    recvBuff = b""
	
    tmpBuff = ""
    
    while len(recvBuff) < length:
		# Attempt to receive bytes
        tmpBuff =  sock.recv(length)
        # The other side has closed the socket
        if not tmpBuff:
            break
        # Add the received bytes to the buffer
        recvBuff += tmpBuff
    return recvBuff