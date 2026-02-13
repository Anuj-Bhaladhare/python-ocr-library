# Import module from Pillow library for image porcessing 
from PIL import Image

class CropAnImage():
    # Class responsible for croping an image

    def __init__(self):
        pass


    def crop_an_image(self):
        # Function for crop am image

        # path to the image file to be crop
        self.image_file = "image_data/image_3.jpg"

        # open the image file and load into memory
        self.image = Image.open(self.image_file)

        # Crop the image
        self.imageCroped = self.image.crop(
            box = (20, 20, 200, 200)
        )

        # Show the croped Image
        self.imageCroped.show()
