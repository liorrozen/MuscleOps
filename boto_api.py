import boto
import boto.ec2
from boto.ec2.connection import EC2Connection
from boto.sqs.connection import SQSConnection
from boto.sqs.message import RawMessage
from boto.s3.connection import S3Connection
from boto.s3.key import Key

# Globals
AWS_ACCESS_KEY = "AKIAIXTVNQVEOVSK33CQ"
AWS_SECRET_KEY = "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"

class Ec2Api( object ):

    def __init__( self ):
        self.conn = EC2Connection(
            aws_access_key_id = AWS_ACCESS_KEY,
            aws_secret_access_key = AWS_SECRET_KEY
        )

        self.instance_id = None

    def create_instance( self, ami = "ami-416b4d28", intance_type = "m1.small" ):
        self.instance_id = self.conn.run_instances( ami, instance_type = intance_type )

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
        self.conn = SQSConnection(
            aws_access_key_id = AWS_ACCESS_KEY,
            aws_secret_access_key = AWS_SECRET_KEY
        )

    def create_queue( self, name = "MuscleOpsQ" ):
        return self.conn.create_queue( name )

    def list_queues( self ):
        return self.conn.get_all_queues()

    def write_message( self, q, msg = "If you're sleepy and you know it; clap your hands!" ):
        m = RawMessage()
        m.set_body( msg )
        q.write( m )

    def read_message( self, q, msg = "If you're sleepy and you know it; clap your hands!" ):
        rs = q.get_messages()
        m = rs[ 0 ].get_body() if len( rs ) else msg
        return m

class S3Api( object ):

    def __init__( self ):
        self.conn = S3Connection( AWS_ACCESS_KEY, AWS_SECRET_KEY )

    def create_bucket( self, name = "muscle.ops.bucket" ):
        return self.conn.create_bucket( name )

    def upload_string( self, bucket, key = "clap", msg = "If you're sleepy and you know it; clap your hands!" ):
        try:
            sqs = SqsApi()
            sqs.create_queue()
            msg = sqs.read_message()
        except Exception as e:
            pass

        k = Key( bucket )
        k.key = key
        k.set_contents_from_string( msg )

#######################################################
def test_ec2_create( ec2 ):
    ec2.create_instance()

def test_ec2_stop( ec2 ):
    ec2.stop_instances( [ "i-88895266" ] )

def test_sqs_run():
    sqs = SqsApi()
    sqs.write_message( sqs.create_queue() )

def test_s3_create_bucket():
    s3 = S3Api()
    s3.upload_string( s3.create_bucket() )


if __name__ == "__main__":
    #ec2 = Ec2Api()
    #test_ec2_create( ec2 )
    #test_ec2_stop( ec2 )
    #test_sqs_run()

    test_s3_create_bucket()
