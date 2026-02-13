# Import the module from Pillow for image processing 
from PIL import Image

class ResizeImage():
    # Class resposible for resizing an image

    def __init__(self):
        # Constructor that stores the image reference (currently unused)
        pass

    
    def resize_img(self):
        # path to the image file to be resized
        self.image_file = "image_data/image_1.jpg"

        # open the image file and load into memory
        self.image = Image.open(self.image_file)

        self.image.show()

        # Display original image dimensions
        print(f"Before: Width = {self.image.width}, Height = {self.image.height} ")

        # Resize the image
        self.image = self.image.resize(
            (
                int(self.image.width // 2),     # New width: half of original width
                int(self.image.height // 2)     # New height: half of original height
            ),
            resample=Image.LANCZOS,             # High-quality downsampling filter
            # box=(20, 20, 100, 100)              # Crop box (left, upper, right, lower)
        )

        # Display the resized image
        self.image.show()

        # Display new image dimentions
        print(f"After: Width = {self.image.width}, Height = {self.image.height} ")

