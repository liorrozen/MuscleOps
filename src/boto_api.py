import boto
from boto.sqs.message import Message
from boto.s3.connection import S3Connection
from boto.s3.key import Key

# Globals
AWS_ACCESS_KEY = "AKIAJGLXJSPCFPNF7UJA",
AWS_SECRET_KEY = "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"

class Ec2Api( object ):

    def __init__( self ):
        self.conn = boto.ec2.connect_to_region(
            "us-west-2",
            aws_access_key_id = AWS_ACCESS_KEY,
            aws_secret_access_key = AWS_SECRET_KEY
        )

    def create_instance( self, ami = "ami-e4c4528d", intance_type = "t1.micro" ):
        self.conn.run_instances( ami, instance_type = intance_type )

    def start_instances( self, instance_ids ):
        instances = self.conn.get_only_instances( instance_ids = instance_ids )
        for instance in instances:
            instance.start()

    def stop_instances( self, instance_ids ):
        self.conn.stop_instances( instance_ids = instance_ids )

    def terminate_instances( self, instance_ids ):
        self.conn.terminate_instances( instance_ids = instance_ids )


class SqsApi( object ):

    def __init__( self ):
        self.conn = boto.sqs.connect_to_region(
            "us-west-2",
            aws_access_key_id = AWS_ACCESS_KEY,
            aws_secret_access_key = AWS_SECRET_KEY
        )

    def create_queue( self, name ):
        return self.conn.create_queue( name )

    def list_queues( self ):
        return self.conn.get_all_queues()

    def write_message( self, msg = "If you're sleepy and you know it; clap your hands!" ):
        m = Message()
        m.set_body( msg )
        q.write( m )


class S3Api( object ):

    def __init__( self ):
        self.conn = S3Connection( AWS_ACCESS_KEY, AWS_SECRET_KEY )

    def create_bucket( self, name ):
        return self.conn.create_bucket( name )

    def upload_string( self, bucket, key = "foobar", msg = "This is S3 Test" ):
        k = Key( bucket )
        k.key = key
        k.set_contents_from_string( msg )
