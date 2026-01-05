import os
from drive_api import download_new_images
from slideshow import Slideshow

FOLDER_ID = "<to be filled in>"  # TODO: fill this in

BACKGROUND_COLOR = "#222"
IMAGE_DIR = "images"
IMAGE_DURATION = 5 * 1000


def main():
    num_new = download_new_images(FOLDER_ID, IMAGE_DIR)
    print(f"downloaded {num_new} new images")

    downloaded_images = os.listdir(IMAGE_DIR)
    im_paths = list(map(lambda fn: f"{IMAGE_DIR}/{fn}", downloaded_images))

    viewer = Slideshow(im_paths=im_paths, pad_color=BACKGROUND_COLOR)
    viewer.start_slideshow(interval=IMAGE_DURATION)
    viewer.start()


if __name__ == "__main__":
    main()
