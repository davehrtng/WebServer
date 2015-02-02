#!/usr/bin/env python

import socket
import sys
from webob import Request

def constructRequestString(method, path):
		"""creates an HTTP request string. method and path are string."""
		request = ""
		
		#e.g. GET /join HTTP/1.1
		request += method 
		request += " /" + path 
		request += " HTTP/1.1\n"
		
		#e.g., Host: thomas.butler.edu
		#User-agent: wumpus-hunter-client-harting 0.0
		#Connection: keep-alive
		request += "Host: thomas.butler.edu\n"
		request += "User-agent: " + "david-client\n"
		request += "Connection: keep-alive\n"
						
		return request

def main():
	server = 'localhost'
	port = 8080

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((server, port))
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	sys.stderr.write("connecting to %s port %s\n" % (server, port))
	
	while True:
		path = raw_input('type the path of the document you want')
		requestString = constructRequestString('GET', path)
		s.send(requestString)
		response = s.recvfrom(1024)
		print(response)
	
	
	s.close()
        

if __name__ == "__main__":
    main()