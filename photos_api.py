import os
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import requests
from googleapiclient.discovery import build
import pickle

# Scopes for Google Photos Library API
SCOPES = ["https://www.googleapis.com/auth/photoslibrary.readonly"]


def authenticate_google_photos():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is created automatically when the authorization flow completes for the first time.
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


def get_photos_from_album(album_id):
    creds = authenticate_google_photos()
    service = build("photoslibrary", "v1", credentials=creds, static_discovery=False)

    page_token = None
    photos = []

    while True:
        response = (
            service.mediaItems()
            .search(
                body={
                    "albumId": album_id,
                    "pageSize": 100,
                    "pageToken": page_token,
                }
            )
            .execute()
        )

        if "mediaItems" in response:
            photos.extend(
                map(
                    lambda item: {
                        "filename": item["filename"],
                        "baseUrl": item["baseUrl"],
                    },
                    response["mediaItems"],
                )
            )

        # Check for a next page token to fetch more results
        page_token = response.get("nextPageToken")
        if not page_token:
            break

    return photos


def fetch_albums():
    """fetch regular and shared albums of user"""

    creds = authenticate_google_photos()
    service = build("photoslibrary", "v1", credentials=creds, static_discovery=False)

    # fetch user-owned and shared albums
    results = service.albums().list(pageSize=50).execute()
    albums = results.get("albums", [])

    # fetch shared albums
    results = service.sharedAlbums().list(pageSize=50).execute()
    shared_albums = results.get("sharedAlbums", [])

    return albums, shared_albums


def download_image(base_url, image_filename, width=None, height=None):
    """download image given base_url and image_filename from Google Photos"""

    if width is not None and height is not None:
        image_url = base_url + f"=w{width}-h{height}"
    else:
        image_url = (
            base_url + "=d"
        )  # `=d` gets the full-resolution image. Use other sizes if needed.

    # Send HTTP GET request to download the image
    response = requests.get(image_url)

    # If the request was successful, write the content to a file
    if response.status_code == 200:
        with open(image_filename, "wb") as file:
            file.write(response.content)
        print(f"Image downloaded: {image_filename}")
    else:
        print(f"Failed to download image: {response.status_code}")


def download_new_images(album_id: str, image_dir: str) -> int:
    """Download all images from album that aren't already downloaded to image_dir"""

    album_photos = get_photos_from_album(album_id)

    os.makedirs(image_dir, exist_ok=True)
    already_downloaded = os.listdir(image_dir)

    num_downloaded = 0

    for i, photo in enumerate(album_photos):
        if photo["filename"] in already_downloaded:
            continue

        download_image(photo["baseUrl"], f"{image_dir}/{photo['filename']}")
        num_downloaded += 1

    return num_downloaded


def photos_api_setup():
    """Gets the Auth token and lists albums with their ids to identify the correct Album ID"""

    authenticate_google_photos()

    print()
    owned_albums, shared_albums = fetch_albums()
    print("OWNED ALBUMS:")
    for album in owned_albums:
        print(f"\t{album['title']} (id: {album['id']})")

    print("\n\nSHARED ALBUMS:")
    for album in shared_albums:
        print(
            f"\t{album['title'] if 'title' in album else '(Untitled)'} (id: {album['id']})"
        )


if __name__ == "__main__":
    photos_api_setup()
