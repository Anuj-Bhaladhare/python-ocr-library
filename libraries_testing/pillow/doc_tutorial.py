import os, sys
from PIL import Image, ImageFilter, ImageEnhance, ImageSequence, PSDraw


class DocumentTutorial():

    def __init__(self):
        pass


    def convert_files_to_jpeg(self, files):
        for infile in files:
            f, e = os.path.splitext(infile)
            outfile = f + ".jpg"

            if infile.lower() != outfile.lower():
                try:
                    with Image.open(infile) as im:
                        im = im.convert("RGB")
                        im.save(outfile, "JPEG")
                        print("File saved:", outfile)
                except OSError as e:
                    print("Cannot convert", infile, "->", e)


    def create_jpeg_thumbnails(self, image, outfile):
        size = (128, 128)

        try:
            image = image.convert("RGB")
            image.thumbnail(size)
            image.save(outfile, "JPEG")
            print("Thumbnail created:", outfile)
        except OSError as e:
            print("Cannot create thumbnail ->", e)


    # Rolling an image
    def rolling_an_image(self, im: Image.Image, delta: int) -> Image.Image:
        """Roll an image sideways."""
        xsize, ysize = im.size

        delta = delta % xsize
        if delta == 0:
            return im

        part1 = im.crop((0, 0, delta, ysize))
        part2 = im.crop((delta, 0, xsize, ysize))
        im.paste(part1, (xsize - delta, 0, xsize, ysize))
        im.paste(part2, (0, 0, xsize - delta, ysize))

        return im


    # Merging images
    def merge(self, im1: Image.Image, im2: Image.Image) -> Image.Image:
        w = im1.size[0] + im2.size[0]
        h = max(im1.size[1], im2.size[1])
        im = Image.new("RGBA", (w, h))

        im.paste(im1)
        im.paste(im2, (im1.size[0], 0))

        return im
    

    # Splitting and merging bands
    def splitting(self, im: Image.Image):
        im = im.convert("RGB")   # 🔑 force 3 channels
        r, g, b = im.split()
        im = Image.merge("RGB", (b, g, r))
        return im
    

    def resize_rotate(self, im: Image.Image):
        out = im.resize((128, 128))
        out = im.rotate(135) # degrees counter-clockwise
        return out
    

    def transposing_an_image(self, im: Image.Image):

        # out = im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)

        # out = im.transpose(Image.Transpose.FLIP_TOP_BOTTOM)

        # out = im.transpose(Image.Transpose.ROTATE_90)

        # out = im.transpose(Image.Transpose.ROTATE_180)

        out = im.transpose(Image.Transpose.ROTATE_270)

        return out

    # Applying filters
    def applying_filters(self, im: Image.Image):

        out = im.filter(ImageFilter.DETAIL)

        return out
    

    # Applying point transforms
    def applying_point_transforms(self, im: Image.Image):
        # multiply each pixel by 20
        out = im.point(lambda i: i * 20)

        return out


    # Processing individual bands
    def processing_individual_bands(self, im: Image.Image):
        # split the image into individual bands
        source = im.split()

        R, G, B = 0, 1, 2

        # select regions where red is less than 100
        mask = source[G].point(lambda i: i < 100 and 255)

        # process the green band
        out = source[R].point(lambda i: i * 0.7)

        # paste the processed band back, but only where red was < 100
        source[R].paste(out, None, mask)

        # build a new multiband image
        im = Image.merge(im.mode, source)

        return im
    
    
    # Enhancing images
    def enhancing_images(self, im: Image.Image):
        enh = ImageEnhance.Contrast(im)

        enh.enhance(1.3).show("30% more contrast")

        return enh
    

    # Reading sequences
    def reading_sequences(self):
        with Image.open("image_data/animation.gif") as im:
            im.seek(1)   # slip to the second frame

            try:
                frame = 0
                while True:
                    im.seek(frame)

                    # do something wit current frame
                    im.show()

                    frame += 1

            except EOFError:
                pass    # end of sequence


    # Writing sequences => Convert multiple images in to GIF image
    def writing_sequences(self):
        # List of image filenames
        image_filenames = [
            "image_data/pass_port_image.png",
            "image_data/image_3.jpg",
            "image_data/book_image_2.jpeg",
            "image_data/image_4.jpg"
        ]

        # open images as an animated GID
        images = [Image.open(filename) for filename in image_filenames]

        # Save the images as an animated GIF
        images[0].save(
            "image_output/animated_hopper.gif",
            append_images = images[1:],
            duration=500,   # duration of each frame in milliseconds
            loop=0          # loop forever
        )


    # Using the Iterator class
    def using_the_Iterator_class(self):

        self.im = Image.open("image_data/animation.gif")

        # # ✅ Example 1: Frame ko grayscale bana ke save karna
        # for i, frame in enumerate(ImageSequence.Iterator(self.im)):
        #     self.gray_frame = frame.convert("L")        # grayscale 
        #     self.gray_frame.save(f"image_output_gif/frame_{i}.png")         


        # # ✅ Example 2: Frame resize + rotate karna
        # for i, frame in enumerate(ImageSequence.Iterator(self.im)):
        #     frame = frame.convert("RGB")
        #     frame = frame.resize((300, 300))
        #     frame = frame.rotate(45)
        #     frame.save(f"image_output_gif/edited_frame_{i}.jpg")



        # ✅ Example 3: Frame se pixel data read karna
        for frame in ImageSequence.Iterator(self.im):
            frame = frame.convert("RGB")
            pixels = frame.load()

            width, height = frame.size
            r, g, b = pixels[0, 0]   # top-left pixel

            print(f"{frame} First pixel RGB:", r, g, b)


    # Python Imaging Library (PIL) includes functions to print images, text and graphics on PostScript printers
    def drawing_postScript(self):

        # 1️⃣ Define the PostScript file (.ps is correct extension)
        self.ps_file = open("image_output/PostScript.ps", "wb")

        # 2️⃣ Create PSDraw object
        ps = PSDraw.PSDraw(self.ps_file)

        # 3️⃣ Start the document
        ps.begin_document()

        # 4️⃣ Page size (A4 in points)
        page_width, page_height = 595, 842

        # 5️⃣ Text settings
        text = "Mr. Hopper"
        font_name = "Helvetica-Bold"
        font_size = 25

        # Approximate text size
        text_width = len(text) * font_size * 0.6
        text_height = font_size

        # Text position (top-center)
        # text_x = (page_width - text_width) // 2
        # text_y = page_height - text_height - 50
        text_x_1 = 85
        text_y_1 = 530

        # 6️⃣ Draw text
        ps.setfont(font_name, font_size)
        ps.text((text_x_1, text_y_1), text)

        # 7️⃣ Load and draw image
        image_path = "image_data/pass_port_image.png"

        with Image.open(image_path) as im:
            im = im.convert("RGB")

            # Resize image to fit page
            im.thumbnail((200, 200))

            # Image position (centered, below text)
            # img_x = (page_width - im.width) // 2
            # img_y = text_y - im.height - 50
            img_x = 50
            img_y = 550


            # Draw image (75 dpi)
            ps.image(
                (img_x, img_y, img_x + im.width, img_y + im.height),
                im,
                75
            )

        # 8️⃣ End document and close file
        ps.end_document()
        self.ps_file.close()






    def document_tutorial(self):

        self.image = Image.open("image_data/pass_port_image.png")
        # print(self.image.format, self.image.size, self.image.mode)
        # self.image.show()

        # =======> Call Self function <========
        # self.convert_files_to_jpeg(self.image)

        self.create_jpeg_thumbnails(self.image, "image_output/output_thumbnail.jpg")

        # rolled_image = self.rolling_an_image( self.image, 300)
        # rolled_image.show()           # preview
        # rolled_image.save("image_output/rolled_image.png")

        # murged_image = self.merge(self.image, self.image)
        # murged_image.show()
        # murged_image.save("image_output/murged_image.png")

        # splitting_image = self.splitting(self.image)
        # splitting_image.show()
        # splitting_image.save("image_output/splitting_image.png")

        # resize_rotate_image = self.resize_rotate(self.image)
        # resize_rotate_image.show()
        # resize_rotate_image.save("image_output/resize_rotate_image.png")

        # transposing_an_img = self.transposing_an_image(self.image)
        # transposing_an_img.show()
        # transposing_an_img.save("image_output/transposing_an_image.png")

        # applying_filters_image = self.applying_filters(self.image)
        # applying_filters_image.show()
        # applying_filters_image.save("image_output/applying_filters_image.png")

        # applying_point_transforms_image = self.applying_point_transforms(self.image)
        # applying_point_transforms_image.show()
        # applying_point_transforms_image.save("image_output/applying_point_transforms_image.png")

        # processing_individual_bands_image = self.processing_individual_bands(self.image)
        # processing_individual_bands_image.show()
        # processing_individual_bands_image.save("image_output/processing_individual_bands_image.png")

        # enhancing_images_img = self.processing_individual_bands(self.image)
        # enhancing_images_img.show()
        # enhancing_images_img.save("image_output/enhancing_images_img.png")

        # self.reading_sequences()

        # self.writing_sequences()

        # self.using_the_Iterator_class()

        # Drawing PostScript
        # self.drawing_postScript()
