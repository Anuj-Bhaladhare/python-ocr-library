from PIL import Image

class WorkingWithImageTutorial():

    def __init__(self):
        pass


    def introduction(self):
        self.image = Image.open("image_data/image_4.jpg")

        print(f"Height  =>  {self.image.height}\n")
        print(f"Width  =>  {self.image.width}\n")
        print(f"Size  =>  {self.image.size}\n")
        print(f"Format  =>  {self.image.format}\n")




    def resize_image(self):

        self.image = Image.open("image_data/image_4.jpg")

        resize_of_new_image = (300, 300)

        self.image.thumbnail(resize_of_new_image)  # Resize image in 300 x 300

        self.image.save('image_output/new_flower_300.jpg')

