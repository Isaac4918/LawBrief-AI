import os
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient

load_dotenv() 

blob_conn = os.getenv("AZURE_BLOB_CONN_STRING")
container_name = os.getenv("BLOB_CONTAINER_NAME")

blob_service = BlobServiceClient.from_connection_string(blob_conn)
container = blob_service.get_container_client(container_name)

def upload_file_to_blob(filename: str, data: bytes):
    blob = container.get_blob_client(filename)
    blob.upload_blob(data, overwrite=True)
    return f"File uploaded: {filename}"
