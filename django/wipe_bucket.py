from boto.s3.connection import S3Connection
import sys
import os
import argparse
import json

parser = argparse.ArgumentParser(description='Delete all keys in a bucket. Connection information is specified in os variable "VCAP_SERVICES"')
parser.add_argument('--force', help='Force execution', action="store_true")

args = parser.parse_args()

VCAP_SERVICES = json.loads(os.environ['VCAP_SERVICES'])
for group in VCAP_SERVICES:
    for service in VCAP_SERVICES[group]:
        if "ecs" in service['name']:
            AWS_S3_HOST = service['credentials']['HOST']
            AWS_ACCESS_KEY_ID = service['credentials']['ACCESS_KEY_ID']
            AWS_SECRET_ACCESS_KEY = service['credentials']['SECRET_ACCESS_KEY']
            BUCKET_NAME = service['credentials']['SECURE_BUCKET']

if not args.force:
    choice = None
    while choice not in ('y', 'n'):
        choice = input('Do you really want to wipe the bucket "%s"? (y/n)' %(BUCKET_NAME))

    if choice == 'n':
        raise SystemExit("aborted by user input")

conn = S3Connection(aws_access_key_id=AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                    host=AWS_S3_HOST
                    )
bucket = conn.get_bucket(BUCKET_NAME)
keys = bucket.get_all_keys()
if not keys:
    print("no keys to delete in bucket: %s" %(BUCKET_NAME))
    raise SystemExit()
result = bucket.delete_keys(keys)
if not result.deleted:
    raise SystemExit("keys not successfully deleted")
#bucket.delete()
print("Deleted all keys in bucket: %s" %(BUCKET_NAME))
