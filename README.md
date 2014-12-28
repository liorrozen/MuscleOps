MuscleOps
=========

**Full body gesture based amazon web services API.**

An Intel Galieo board connected to an accelerometer module sends  movement data via a socket server to an EC2 instance. The instance deciphers the data as gestures and makes API calls to Amazon's web services API.
The gestures can perform tasks such as:

- Starting/Stopping an EC2 instance.
- Creating an SQS queue
- Push messages to the newly created queue
- Create an S3 bucket
- Backup the contents of an SQS queue to the S3 bucket

Live demo - https://www.youtube.com/watch?v=LB5UOkQZCrw
