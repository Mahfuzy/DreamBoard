from storages.backends.s3boto3 import S3Boto3Storage

class SupabaseStorage(S3Boto3Storage):
    def __init__(self, *args, **kwargs):
        kwargs['access_key'] = os.getenv('SUPABASE_KEY')
        kwargs['bucket_name'] = 'media'
        kwargs['endpoint_url'] = os.getenv('SUPABASE_URL')
        super().__init__(*args, **kwargs)