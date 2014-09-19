#! /usr/bin/python

import SocketServer
from levenshtein import MuscleOps
import ast

from boto_api import *


class TCPSocketServer( SocketServer.BaseRequestHandler ):
   
    def handle( self ):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv( 1024 ).strip()
        #print "Recieved: %s" % self.data

	pattern = ast.literal_eval( self.data )

	direction = MuscleOps().gesture( pattern )

	{
		"up": Ec2Api().create_instance ,
		"down": Ec2Api().stop_instance ,
		"left": SqsApi().create_queue().write_message ,
		"right": S3Api().upload_string 
	}[ direction ]()

	print direction

if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 9999

    print "Create socket server for TCP"
    SocketServer.TCPServer.allow_reuse_address = True
    server = SocketServer.TCPServer( ( HOST, PORT ), TCPSocketServer )
    print "Socket server was created"
    server.serve_forever()
