'''
	Name:	prog1_server.py
	
	Brief:	This program acts as a simple python server
		and responds to http get requests.

	By:	Daniel Nix

	Date:	2/28/2014

	For: 	Networking (CSC 492)

	Description:	
		This python script acts as a server to 
		send html files using http protocols. 
		It sets up a socket at port 9876 and 
		listens for incoming http requests. Upon
		receiving a request the server tries to
		find the file requested and serves it to
		the client. If the file is not found a 
		404 Not Found response is sent and an
		appropriate 404.html page is presented.

		The server runs indefinitely and has no
		elegant way of closing. The most effective
		method to close the server is using Ctrl-C
		from the command line.

'''


#import socket module to use sockets
from socket import *
#import threading to use threads
import threading

#create a socket object for the server to use
serverSocket = socket(AF_INET, SOCK_STREAM) 
#Prepare a sever socket
#Set and fix (bind) the port number
serverPort = 9876 
serverSocket.bind(('',serverPort))
#Start the server by letting it listen for requests.
serverSocket.listen(1)

def processRequest( connectionSocket, addr ):
	'''
	Funtion:	processRequest
	Arguments:
		connectionSocket: socket connection to client
		addr: ip address of client
	Description:
		Process Request gets a client socket and 
		processes a request incoming from that client.
			  	
	'''

	try:
		# Wait for an incoming request
		message = connectionSocket.recv(1024) 
		# Get the name of the file requested
		filename = message.split()[1] 
		# Open the file
		f = open(filename[1:]) 
		# Read the file's contents into a string
		outputdata = f.read()
	
		#Send one HTTP header line into socket 
		connectionSocket.send( b"HTTP/1.1 200 OK \r\n" )

		#Send the content of the requested file to the client 
		for i in range(0, len(outputdata)): 
			connectionSocket.send( str.encode(outputdata[i]) ) 

		#Close the client's socket
		connectionSocket.close() 

	except IOError: 
		#Send response message for file not found 
		# Open the 404 file
		f = open("404.html")
		# Read the 404 file
		outputdata = f.read()

		# Send the 404 response
		connectionSocket.send( b"HTTP/1.1 404 Not Found \r\n")
	
		# Send the 404 file
		for i in range(0, len(outputdata)):
			connectionSocket.send( str.encode(outputdata[i]))
		
		#Close client socket 
		connectionSocket.close()
	
	
#Infinite loop for server to run forever to process requests
while True: 
	#Establish the connection 
	connectionSocket, addr = serverSocket.accept() 

	#Creat a thread to process the request	
	threading.Thread(	target=processRequest, \
        			args=(connectionSocket, addr), \
    				).start()

#Close the Server's connection socket		
serverSocket.close() 	



