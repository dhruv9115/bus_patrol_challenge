from flask import Flask, render_template, request
import logging
import boto3
from botocore.exceptions import ClientError

app = Flask(__name__)


def create_bucket(bucket_name, region=None):
    """Create an S3 bucket in a specified region
    If a region is not specified, the bucket is created in the S3 default
    region (us-east-1).
    :param bucket_name: Bucket to create
    :param region: String region to create bucket in, e.g., 'us-west-2'
    :return: True if bucket created, else False
    """

    print("Bucket Name: " + bucket_name)
    message = "Bucket Created with name: " + bucket_name
    # Retrieve the list of existing buckets
    s3 = boto3.client('s3')
    response = s3.list_buckets()

    # Output the bucket names
    # print('Existing buckets:')
    bucket_exists = False
    for bucket in response['Buckets']:
        # print(f'  {bucket["Name"]}')
        if bucket["Name"] == bucket_name:
            print("Bucket already exists")
            bucket_exists = True
            message = f"Bucket ${bucket_name} already exists"
            # Create bucket
    if not bucket_exists:
        try:
            if region is None:
                s3_client = boto3.client('s3')
                s3_client.create_bucket(Bucket=bucket_name)
                message = "Bucket Created with name: " + bucket_name
            else:
                s3_client = boto3.client('s3', region_name=region)
                location = {'LocationConstraint': region}
                s3_client.create_bucket(Bucket=bucket_name,
                                        CreateBucketConfiguration=location)
                message = "Bucket Created with name: " + bucket_name
        except ClientError as e:
            logging.error(e)
            return "ClientError"
    return message


@app.route('/')
def run_s3_create():
    return '''Suffix this URL with /create_bucket/<BUCKET NAME>'''


@app.route('/create_bucket/<bucket_name>')
def create_s3_bucket(bucket_name):
    return create_bucket(bucket_name=bucket_name)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
