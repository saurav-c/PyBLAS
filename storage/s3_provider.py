from .storage_provider import StorageProvider

import boto3

class S3Provider(StorageProvider):
    def __init__(self, aws, bucket):
        self.auth = aws
        self.bucket = bucket
        self.s3_conn = None

    def get(self, funcname):
        return self._get_s3_conn().Object(self.bucket, 'funcs/'
            + funcname).get()['Body'].read()

    def put(self, funcname, obj):
        self._get_s3_conn().Bucket(self.bucket).put_object(Key='funcs/'
            + funcname, Body=obj, ACL='public-read')

    def get_list(self, prefix):
        bucket = self.get_s3_conn().Bucket(self.bucket)
        result = []
        prefix = "funcs/" + prefix

        for f in bucket.objects.all():
            if f.key.startswith(prefix):
                result.append(f.key[6:])

        return result

    def remove(self, funcname):
        self.get_s3_conn().Object(self.bucket, 'funcs/'
            + funcname).delete()

    def _get_s3_conn(self):
        if self.s3_conn == None:
            s3 = boto3.resource('s3',
                    aws_access_key_id=self.auth['access_key_id'],
                    aws_secret_access_key=self.auth['secret_access_key'])

            self.s3_conn = s3

        return self.s3_conn

