import socket


def prepareSize(length: int, byteLength: int = 10):
    lenStr = str(length)
    while len(lenStr) < byteLength:
        lenStr = "0" + lenStr
    return lenStr


def sendData(sock: socket.socket, data: str):
    numSent = 0
    # Send the data!
    bytesToSend = data.encode()
    # in case of an error sending bytes, keep sending the remaining bytes
    while numSent < len(bytesToSend):
        numSent += sock.send(bytesToSend[numSent:])


def sendFile(sock: socket.socket, fileName: str):
    try: 
        fileInput = open(fileName, 'r')
        fileData = fileInput.read()

        if fileData:
            dataSizeStr = prepareSize(len(fileData))
            # Prepend the size of the data to the
            # file data.
            fileData = dataSizeStr + fileData
            sendData(sock, fileData)
            
        fileInput.close()
        return 0
    except FileNotFoundError:
        err = "FAILURE"
        errSizeStr = prepareSize(len(err))
        errData = errSizeStr + err
        sendData(sock, errData)
        return -1


def recvData(sock: socket.socket, length: int):
    recvBuff = b""
	
    tmpBuff = ""
    
    while len(recvBuff) < length:
		# Attempt to receive bytes
        tmpBuff = sock.recv(length)
        # The other side has closed the socket
        if not tmpBuff:
            break
        # Add the received bytes to the buffer
        recvBuff += tmpBuff
    return recvBuff