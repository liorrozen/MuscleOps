#! /usr/bin/python

import SocketServer
from levenshtein import MuscleOps
import ast

from boto_api import *


class TCPSocketServer( SocketServer.BaseRequestHandler ):

    ec2 = Ec2Api()
   
    def handle( self ):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv( 1024 ).strip()
        #print "Recieved: %s" % self.data

	pattern = ast.literal_eval( self.data )

	direction = MuscleOps().gesture( pattern )

	if direction == "up":
		self.ec2.create_instance()

	if direction == "down":
		self.ec2.stop_instances( ["i-7abb6094"] )

	if direction == "left":
	        sqs = SqsApi()
	        sqs.write_message( sqs.create_queue() )

	if direction == "right":
	        s3 = S3Api()
	        s3.upload_string( s3.create_bucket() )

	print direction

if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 9999

    print "Create socket server for TCP"
    SocketServer.TCPServer.allow_reuse_address = True
    server = SocketServer.TCPServer( ( HOST, PORT ), TCPSocketServer )
    print "Socket server was created"
    server.serve_forever()
