# CPSC 471 Programming Assignment
Group5 -  Members: Diego Barrales, Tommy Ly, Kevin Cacho

## Group Memembers

Name: Tommy Ly       
Email Address: lytommy321@csu.fullerton.edu

Name: Diego Barrales      
Email Address: diego.barrales@csu.fullerton.edu

Name: Kevin Cacho     
Email Address: kicacho@csu.fullerton.edu 

### Programming Language

The programming language we used is **Python**

## Execution

1. Download our zip file **final-project-group5.zip** from the submission on Canvas to your desktop(or where ever you want the folder to be located) 
2. Upzip the file
    * when you unzip the file, it should create a folder called **final-project-group5**
3. Open two terminals and head to that directory on both of them using the `cd` command

You can double check you have the correct files by using the `ls` command and you should have the following files and folders...
```
clientfiles
serverfiles
.gitignore
datatransfer.py
README.md
server.py
socketClient.py
``` 

### If you do not have python installed

4. Go to [python.org](https://www.python.org/) and download the lastest version onto your device

### Assuming you have python installed
4. On the first terminal, run the server with:

        python3 server.py <ANY PORT NUMBER>
        For example: python3 server.py 1234
   *If you dont properly close the running process by using keyboard interrupt or quit command then try using another port number if an error occurs*

6. On the second terminal, run the client with:

        python3 socketClient.py <SERVER NAME> <SAME PORT NUMBER>
        For example: python3 socketClient.py localhost 1234

* You have to input **localhost** for the `<SERVER NAME>` and the **same** port number used to run the server

Once you run these two commands on different terminals, you should be connected and be able to run the ftp commands on the client terminal: `get`, `put`, `ls`, and `quit`  

*ONLY WORKS WITH .txt FILES* 

        Example output including the commands: 
      ftp > ls
      Files in Server:
      - file1.txt
      - put.txt
      - file2.txt
      ftp > get file1.txt
      Getting file1.txt from server
      Saving the file data to `clientfiles/file1.txt`
      Data transfer complete! Filename: file1.txt, Bytes Transferred: 13
      ftp > put
      ftp > Enter File Name: put.txt
      putting put.txt to server
      ftp > quit

For "get" and "put" commands the base file must be properly located in the directory in order to be functional.
So for "get" there must be an appropriate file on the serverside.
For the "put" command, there should be an appropriate file on the client side.
