from flask import Flask, request, jsonify
from workflow import main_workflow
import tempfile
import os
import shutil
import io
import re
from flask_cors import CORS

from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

app = Flask(__name__)
CORS(app)

# === Google Drive Auth Config ===
CLIENT_SECRET_FILE = 'client_secret.json'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

# === Helper to get Drive Service ===
def get_drive_service():
    creds = None
    token_file = 'token.json'
    # https://drive.google.com/file/d/1Hpac7k5O-QPojkV1BD3o7TcIuISwcEk3/view?usp=drive_link

    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=8080)
        with open(token_file, 'w') as token:
            token.write(creds.to_json())

    return build(API_NAME, API_VERSION, credentials=creds)

def download_drive_file(service_obj, file_id, local_file_name):
    
    try:
        # Request the media content of the file
        request = service_obj.files().get_media(fileId=file_id)
        
        # Create an in-memory binary stream to store the downloaded content temporarily
        file_handle = io.BytesIO()
        
        # Initialize the downloader with the file handle and request
        downloader = MediaIoBaseDownload(file_handle, request)
        
        done = False
        while done is False:
            # Retrieve the next chunk of the file
            status, done = downloader.next_chunk()
            # Print download progress
            print(f"Downloading '{local_file_name}': {int(status.progress() * 100)}%.")
        
        # After download is complete, reset the file handle's position to the beginning
        # so that its content can be read and written to a local file.
        file_handle.seek(0)
        
        # Write the downloaded content from the in-memory stream to a local file
        with open(local_file_name, 'wb') as f:
            f.write(file_handle.read())
            # The 'with' statement automatically closes the file, so f.close() is not needed.
            
        print(f"File '{local_file_name}' downloaded successfully.")
        return True
    
    except HttpError as error:
        print(f"Error downloading '{local_file_name}' (ID: {file_id}): {error}")
        print("Please check: 1. If the file ID is correct. 2. If the file exists. 3. If your authenticated Google account has permission to access this file.")
        return False
    except Exception as e:
        print(f"An unexpected error occurred during download of '{local_file_name}': {e}")
        return False

# === Helper to extract File ID from Google Drive URL ===
def extract_drive_file_id(drive_url):
    # Try to extract using different common patterns
    patterns = [
        r"/d/([a-zA-Z0-9_-]+)",                  # /d/FILE_ID
        r"id=([a-zA-Z0-9_-]+)",                  # id=FILE_ID
        r"/file/d/([a-zA-Z0-9_-]+)"              # /file/d/FILE_ID
    ]
    for pattern in patterns:
        match = re.search(pattern, drive_url)
        if match:
            return match.group(1)
    return None



@app.route('/api/extract-mcq', methods=['POST'])
def extract_mcq():
        
    try:
        service = get_drive_service()

        # Case 1: Google Drive Link
        if request.json and 'pdfUrl' in request.json:
            drive_url = request.json['pdfUrl']
            file_id = extract_drive_file_id(drive_url)
            if not file_id:
                return jsonify({"error": "Invalid Google Drive URL"}), 400
            file_name = f"{file_id}.pdf"
            isDownloaded = download_drive_file(service, file_id, file_name)
            if not isDownloaded:
                return jsonify({"error": "Failed to download file from Google Drive"}), 500
            pdf_path = file_name
        else:
            print("Either no driveUrl provided or invalid format.")

        # Process PDF with your existing logic
        mcqs = main_workflow(pdf_path)
        print(f"[DEBUG] Extracted MCQs count: {len(mcqs)}")

        return jsonify({"questions": mcqs}), 200

    except Exception as e:
        print(f"[ERROR] Exception during PDF processing: {e}")
        return jsonify({"error": str(e)}), 500

    finally:
        if 'pdf_path' in locals() and os.path.exists(pdf_path):
            os.remove(pdf_path)

if __name__ == "__main__":
    app.run(debug=True)
