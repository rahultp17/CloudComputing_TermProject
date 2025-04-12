from google.cloud import storage

# def upload_to_bucket(bucket_name, source_file_path, destination_blob_name):
#     # Load credentials from file
#     creds = service_account.Credentials.from_service_account_file(
#         "C:/Users/rahul/Downloads/smart-pride-456601-t3-9225d179d815.json"
#     )

#     # Initialize client with creds
#     storage_client = storage.Client(credentials=creds)
#     bucket = storage_client.bucket(bucket_name)
#     blob = bucket.blob(destination_blob_name)

#     # Upload and make it public
#     blob.upload_from_filename(source_file_path)
#     blob.make_public()

#     return blob.public_url  # ✅ Returns public HTTPS URL

def upload_to_bucket(bucket_name, source_file_path, destination_blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_path)

    # ⛔️ Do NOT use: blob.make_public()

    return blob.public_url  # This still returns a valid URL, not necessarily public

