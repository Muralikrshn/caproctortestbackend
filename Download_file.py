import os
import io

# Import necessary libraries for Google Drive API authentication
# If these are not installed, run:
# pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib google-resumable-media
import google.auth
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload # Used for downloading
from googleapiclient.http import MediaFileUpload # Included for completeness if you want to upload

# --- Configuration Constants ---
# Path to your Google Cloud Console downloaded client secret JSON file
# Make sure this file is in the same directory as your script.
CLIENT_SECRET_FILE = 'client_secret.json'
API_NAME = 'drive'
API_VERSION = 'v3'
# Define the necessary OAuth 2.0 scopes.
# 'https://www.googleapis.com/auth/drive' gives full access.
# Consider narrower scopes if possible, e.g., 'https://www.googleapis.com/auth/drive.readonly' for download only,
# or 'https://www.googleapis.com/auth/drive.file' for app-specific file access.
SCOPES = ['https://www.googleapis.com/auth/drive']


# --- Authentication Function ---
def get_drive_service():
    """
    Authenticates with Google Drive API and returns a service object.
    Handles token refreshing and browser-based authorization for first-time use.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    token_file = 'token.json'
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)
    
    # If there are no (valid) credentials available, or if they are expired
    # but a refresh token exists, refresh them. Otherwise, prompt the user to log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # This initiates the OAuth 2.0 flow. It will open a browser window
            # and prompt the user to grant permissions to the application.
            # `port=0` tells it to find any available port.
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for the next run to avoid re-authenticating
        with open(token_file, 'w') as token:
            token.write(creds.to_json())
    
    # Build and return the Google Drive API service object
    return build(API_NAME, API_VERSION, credentials=creds)


# --- Core Download Function ---
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


# --- Main Execution Block ---
if __name__ == "__main__":
    print("--- Starting Google Drive API Operations ---")
    
    # 1. Get the authenticated Google Drive service object
    # This will initiate the browser-based OAuth flow if token.json is not found or is expired.
    drive_service = get_drive_service()
    print("Google Drive service created successfully.")

    # 2. Define the files you want to download
    # Replace 'YOUR_FILE_ID_HERE' with the actual IDs of the files you want to download.
    # Ensure these files are accessible by the Google account you authenticated with.
    files_to_download_info = [
        {'id': '1Hpac7k5O-QPojkV1BD3o7TcIuISwcEk3', 'name': 'cpu1-2merged.pdf'},
        # Add more files here if needed:
        # {'id': 'ANOTHER_FILE_ID', 'name': 'another_document.docx'},
    ]

    # 3. Loop through the list and download each file
    print("\n--- Initiating File Downloads ---")
    for file_info in files_to_download_info:
        file_id = file_info['id']
        file_name = file_info['name']
        
        download_drive_file(drive_service, file_id, file_name)
    
    print("\n--- All download operations attempted. ---")
    print("Check your script's directory for the downloaded files.")