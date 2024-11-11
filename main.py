from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from datetime import datetime
import os

class PhotoReader:
	def __init__(self):
		self.support_formats = ['.jpg','.jpeg','.png','.heic']

	def get_labeled_metadata(self, image_path):
		try:
			with Image.open(image_path) as img:
				exif = img.getexif()
				
				if not exif:
					return {"error": No EXIF metadatafound}

				labeled_metadata = {}
				labeled_metadata["filename"] = os.path.basename(image_path)
        labeled_metadata["file_size"] = f"{os.path.getsize(image_path) / (1024*1024):.2f} MB"
        labeled_metadata["image_size"] = f"{img.size[0]}x{img.size[1]}"
        labeled_metadata["format"] = img.format

				for tag_id in exif:
					tag = TAGS.get(tag_id, tag_id)
					data = exif[tag_id]
