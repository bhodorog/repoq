import boto


class MemoryBackend(object):
    def __init__(self, pkgs=[]):
        self.pkg_list = pkgs

    def gen_pksg(self, ):
        """ generator of names of packages present in repository.
        Package name is without extension."""
        return (p for p in self.pkg_list)


class S3Backend(object):
    def __init__(self, bucket, **kwargs):
        self.bucket = boto.connect_s3(**kwargs).get_bucket(bucket)

    def gen_pksg(self, ):
        """ generator of names of packages present in repository.
        Package name is without extension."""
        return (k.name.rstrip(".tag.gz") for k in self.bucket.list())

