import boto3

# Set up AWS credentials and S3 clients for both accounts
source_access_key = ''
source_secret_key = ''
# source_session_token = 'your-source-session-token' # Optional, only if you're using temporary credentials
source_s3 = boto3.client('s3', aws_access_key_id=source_access_key, aws_secret_access_key=source_secret_key) # , aws_session_token=source_session_token
source_bucket_name = ''

destination_access_key = ''
destination_secret_key = ''
# destination_session_token = 'your-destination-session-token' # Optional, only if you're using temporary credentials
destination_s3 = boto3.client('s3', aws_access_key_id=destination_access_key, aws_secret_access_key=destination_secret_key) # , aws_session_token=destination_session_token
destination_bucket_name = ''

# List all objects in the source bucket
objects = source_s3.list_objects(Bucket=source_bucket_name)['Contents']

# Copy each object to the destination bucket and set it as publicly accessible
for obj in objects:
    # Check if the object is an image (you may need to adjust this condition based on your specific use case)
    # if obj['Key'].lower().endswith('.jpg') or obj['Key'].lower().endswith('.jpeg') or obj['Key'].lower().endswith('.png'):

    # Copy the object to the destination bucket
    copy_source = {'Bucket': source_bucket_name, 'Key': obj['Key']}
    destination_s3.copy_object(CopySource=copy_source, Bucket=destination_bucket_name, Key=obj['Key'])
    
    # Set the object ACL to public-read
    destination_s3.put_object_acl(ACL='public-read', Bucket=destination_bucket_name, Key=obj['Key'])
