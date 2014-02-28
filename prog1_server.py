#import socket module 
from socket import * 

serverSocket = socket(AF_INET, SOCK_STREAM) 
#Prepare a sever socket
serverPort = 9876 
serverSocket.bind(('',serverPort))
serverSocket.listen(1)

def processRequest( connectionSocket, addr ):
	try:
		print( "Waiting for a request..." )
		
		message = connectionSocket.recv(1024) 
		print( "Got request..." )
		
		print( "Message: ", message )
		if len( message ) >  0:
			filename = message.split()[1] 
			f = open(filename[1:]) 
			outputdata = f.read()
			print( "Read file: ", filename[1:] )

		else:
			raise IOError("No Message Data")
		#Send one HTTP header line into socket 
		connectionSocket.send( b"HTTP/1.1 200 OK \r\n" )
		print( "Sent 200 OK response..." )

		#Send the content of the requested file to the client 
		for i in range(0, len(outputdata)): 
			connectionSocket.send( str.encode(outputdata[i]) ) 


		print( "Sent file: ", filename[1:]  )
		connectionSocket.close() 
		print( "Closed connectionSocket. SERVED " )

	except IOError: 
		print( "Hit exception block..." )

		#Send response message for file not found 
		f = open("404.html")
		outputdata = f.read()
		print( "Read file: 404.html" )

		connectionSocket.send( b"HTTP/1.1 404 Not Found \r\n")
		print( "Sent 404 Not Found..." )
	
		for i in range(0, len(outputdata)):
			connectionSocket.send( str.encode(outputdata[i]))
		print( "Sent 404.html..." )
		
		#Close client socket 
		connectionSocket.close()
		print( "Closed connectionSocket. 404" )
	
	

while True: 
	#Establish the connection 
	print('\n\nReady to serve...') 
	connectionSocket, addr = serverSocket.accept() 
	processRequest( connectionSocket, addr )
	
		
serverSocket.close() 	
print( "Closed serverSocket. Goodbye." )


