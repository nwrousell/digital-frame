import os
from photos_api import download_new_images
from slideshow import Slideshow

ALBUM_ID = "APzSpbuJ3_T72v6E0tyJykeB7W4xxySa1Z9oHi33fUMcIBDcPb0D90MXeno296h5oacR4y9tX8-1"  # Digital Frame (Parents)

BACKGROUND_COLOR = "#1919"
IMAGE_DIR = "images"
IMAGE_DURATION = 5 * 1000


def main():
    num_new = download_new_images(ALBUM_ID, IMAGE_DIR)
    print(f"downloaded {num_new} new images")

    downloaded_images = os.listdir(IMAGE_DIR)
    im_paths = list(map(lambda fn: f"{IMAGE_DIR}/{fn}", downloaded_images))

    viewer = Slideshow(im_paths=im_paths, pad_color=BACKGROUND_COLOR)
    viewer.start_slideshow(interval=IMAGE_DURATION)
    viewer.start()


if __name__ == "__main__":
    main()
