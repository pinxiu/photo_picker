import logging
import os
import sys
from PIL import Image
from pillow_heif import register_heif_opener

VALID_IMAGE_TYPES = [".jpg", ".gif", ".png", ".heic"]

logger = logging.getLogger(__name__)


def score_photo(img):
    pixel_value = img[0].getpixel((0, 0))
    logger.info(pixel_value)
    return sum(pixel_value) / (255 * 3)


def list_images_from_directory(input_dir):
    imgs = []
    for f in os.listdir(input_dir):
        logger.info(f)
        ext = os.path.splitext(f)[1]
        if ext.lower() not in VALID_IMAGE_TYPES:
            continue
        imgs.append((Image.open(os.path.join(input_dir, f)), f))
    return imgs


def write_photo(img, filename, output_dir):
    img.save(os.path.join(output_dir, filename))


def choose_photos(input_dir="input_photos", output_dir="output_photos"):
    logger.info("Choose photos")
    best_img = max(list_images_from_directory(input_dir), key=score_photo)
    write_photo(best_img[0], best_img[1], output_dir)


if __name__ == "__main__":
    logging.basicConfig(filename="photo_picker.log", level=logging.INFO)
    register_heif_opener()
    choose_photos(input_dir=sys.argv[1])
    logger.info("Done")
