#! /usr/bin/python

import SocketServer
from levenshtein import MuscleOps
import ast


class TCPSocketServer( SocketServer.BaseRequestHandler ):
   
    def handle( self ):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv( 1024 ).strip()
        print "Recieved: %s" % self.data

	pattern = ast.literal_eval( self.data )

	direction = MuscleOps().gesture( pattern )

	print direction

if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 9999

    print "Create socket server for TCP"
    SocketServer.TCPServer.allow_reuse_address = True
    server = SocketServer.TCPServer( ( HOST, PORT ), TCPSocketServer )
    print "Socket server was created"
    server.serve_forever()
