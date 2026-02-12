import boto3
from app.core.config import settings
import uuid
import logging

logger = logging.getLogger(__name__)

class StorageService:
    def __init__(self):
        # In a real scenario, use aioboto3 for async
        self.s3 = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION
        )
        self.bucket = settings.S3_BUCKET_NAME

    def upload_data(self, data: bytes, content_type: str = "application/octet-stream") -> str:
        """
        Uploads bytes and returns a presigned URL.
        
        Args:
            data: The bytes to upload
            content_type: MIME type of the data
            
        Returns:
            Presigned URL for accessing the uploaded file
            
        Raises:
            ValueError: If data is invalid
            RuntimeError: If upload fails
        """
        if not isinstance(data, bytes):
            raise ValueError("Data must be bytes")
        
        if len(data) == 0:
            logger.warning("Uploading empty file to S3")
        
        if len(data) > 100 * 1024 * 1024:  # 100MB limit
            raise ValueError("File too large (max 100MB)")
        
        object_name = str(uuid.uuid4())
        
        try:
            self.s3.put_object(
                Bucket=self.bucket,
                Key=object_name,
                Body=data,
                ContentType=content_type
            )
            logger.info(f"Uploaded file to S3: {object_name} ({len(data)} bytes)")
            return self.generate_presigned_url(object_name)
        except Exception as e:
            logger.error(f"S3 upload error: {e}")
            raise RuntimeError(f"Failed to upload to S3: {str(e)}")

    def generate_presigned_url(self, object_name: str, expiration: int = 3600) -> str:
        """
        Generate a presigned URL for accessing an S3 object.
        
        Args:
            object_name: The S3 object key
            expiration: URL expiration time in seconds (default 1 hour)
            
        Returns:
            Presigned URL
            
        Raises:
            RuntimeError: If URL generation fails
        """
        try:
            response = self.s3.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket, 'Key': object_name},
                ExpiresIn=expiration
            )
            return response
        except Exception as e:
            logger.error(f"S3 presign error: {e}")
            raise RuntimeError(f"Failed to generate presigned URL: {str(e)}")
