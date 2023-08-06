from PIL import Image

class Resquare:
    def __init__(self,in_file,out_file,target_width):
        """
        in_file: location of original image file
        out_file: location of output file
        target_width: target dimensions of output file
        """
        self.image = Image.open(in_file)
        background_color = self.determine_background_color(self.image)
        square_image = self.resquare(self.image,background_color).resize((target_width, target_width), Image.LANCZOS)
        square_image.save(out_file, quality=100)

    def determine_background_color(self,image):
        """
        Infer logo background color of upper left corner pixel 
        """
        width = image.width
        height = image.height
        if image.mode == 'RGB':
            r, g, b = image.getpixel((0, 0))
        else:
            self.image = self.image.convert('RGB')
            image = self.image
            r, g, b = image.getpixel((0, 0))
        return (r,g,b)

    def resquare(self,image,background_color):
        width, height = image.size
        if width == height:
            return image
        elif width > height:
            result = Image.new(image.mode, (width, width), background_color)
            result.paste(image, (0, (width - height) // 2))
            return result
        else:
            result = Image.new(image.mode, (height, height), background_color)
            result.paste(image, ((height - width) // 2, 0))
            return result

