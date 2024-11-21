from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS


class ExifReader:
    def __init__(self, image_path):
        self.image_path = image_path
        self.raw_data = None
        self.gps_data = None
        self.exif_data = None
        
    def load_image(self):
        try:
            with Image.open(self.image_path) as img:
                self.raw_data = img._getexif()
                if self.raw_data:
                    self.exif_data = self.get_exif(self.raw_data)
                    self.gps_data = self.get_gps(self.raw_data)
        
        
        except (AttributeError, KeyError, IndexError, OSError) as e:
            print(f"Error processing image: {e}")
    
    @staticmethod
    def get_exif(exif):
        exif_wl = ['Make','Model','DateTime']
        temp = {}
        exif_data = {}
        
        for key, value in exif.items():
            temp[TAGS.get(key,key)] = value
        
        # literally no idea why it didnt work when i did this in one loop but whatever...
        for key, value in temp.items():
            if key in exif_wl:
                exif_data[TAGS.get(key,key)] = value
        
        return exif_data
    
    @staticmethod
    def get_gps(exif):
        gps_wl = ['GPSLatitude','GPSLongitude','GPSAltitude',]
        temp = {}
        gps_data = {}
        
        if not exif:
            return {}
        
        for key, value in exif.items():
            decoded = TAGS.get(key,key)
            if decoded == "GPSInfo":
                for k in value:
                    gps_decoded = GPSTAGS.get(k,k)
                    temp[gps_decoded] = value[k]

        # again dono why this had to be done outside first loop...
        for key, value in temp.items():
            if key in gps_wl:
                gps_data[TAGS.get(key,key)] = value

        return gps_data
    
    def serial_print(self):
        if not self.exif_data:
            print("No EXIF data to display...")
            return
        
        print("EXIF DATA:")
        for key, value in self.exif_data.items():
            print(f"{key:25}: {value}")
            
        print("\nGPS DATA:")
        if self.gps_data:
            for key, value in self.gps_data.items():
                print(f"{key:25}: {value}")
        else:
            print("No GPS data...")    
        

if __name__ == "__main__":
    image_path = input("Type image path: ")
    processor = ExifReader(image_path)
    processor.load_image()
    processor.serial_print()