from flask import Blueprint, request
from app.utils.gcs import upload_to_bucket
import os

gcs_upload = Blueprint('gcs_upload', __name__)

@gcs_upload.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    file_path = file.filename
    file.save(file_path)

    bucket_name = 'weather-app-storage-rahul'  # ✅ Your bucket
    uploaded_url = upload_to_bucket(bucket_name, file_path, file_path)

    os.remove(file_path)  # clean up

    return f"✅ Uploaded to: {uploaded_url}", 200
