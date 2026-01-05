import os
import io
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import pickle

# Scopes for Google Drive API (readonly access)
SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]


def authenticate_google_drive():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token_file:
            creds = pickle.load(token_file)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.pickle", "wb") as token_file:
            pickle.dump(creds, token_file)
    return creds


def get_images_from_folder(folder_id: str) -> list[dict]:
    """Get all image files from a Google Drive folder."""
    creds = authenticate_google_drive()
    service = build("drive", "v3", credentials=creds)

    page_token = None
    images = []

    # Query for image files in the specified folder
    query = f"'{folder_id}' in parents and mimeType contains 'image/'"

    while True:
        response = (
            service.files()
            .list(
                q=query,
                fields="nextPageToken, files(id, name)",
                pageSize=100,
                pageToken=page_token,
            )
            .execute()
        )

        files = response.get("files", [])
        images.extend([{"id": f["id"], "filename": f["name"]} for f in files])

        page_token = response.get("nextPageToken")
        if not page_token:
            break

    return images


def fetch_folders():
    """Fetch folders accessible to the user."""
    creds = authenticate_google_drive()
    service = build("drive", "v3", credentials=creds)

    # Query for folders only
    query = "mimeType = 'application/vnd.google-apps.folder'"
    results = (
        service.files().list(q=query, fields="files(id, name)", pageSize=50).execute()
    )
    folders = results.get("files", [])

    return folders


def download_image(service, file_id: str, image_filename: str):
    """Download an image from Google Drive given its file ID."""
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)

    done = False
    while not done:
        status, done = downloader.next_chunk()

    # Write the downloaded content to file
    with open(image_filename, "wb") as f:
        fh.seek(0)
        f.write(fh.read())

    print(f"Image downloaded: {image_filename}")


def download_new_images(folder_id: str, image_dir: str) -> int:
    """Download all images from folder that aren't already downloaded to image_dir."""
    creds = authenticate_google_drive()
    service = build("drive", "v3", credentials=creds)

    folder_images = get_images_from_folder(folder_id)

    os.makedirs(image_dir, exist_ok=True)
    already_downloaded = os.listdir(image_dir)

    num_downloaded = 0

    for image in folder_images:
        if image["filename"] in already_downloaded:
            continue

        download_image(service, image["id"], f"{image_dir}/{image['filename']}")
        num_downloaded += 1

    return num_downloaded


def drive_api_setup():
    """Gets the Auth token and lists folders to identify the correct Folder ID."""
    authenticate_google_drive()

    print()
    folders = fetch_folders()
    print("ACCESSIBLE FOLDERS:")
    for folder in folders:
        print(f"\t{folder['name']} (id: {folder['id']})")

    print("\nTip: You can also get the folder ID from the Google Drive URL:")
    print("https://drive.google.com/drive/folders/YOUR_FOLDER_ID_HERE")


if __name__ == "__main__":
    drive_api_setup()
