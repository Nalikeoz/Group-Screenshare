from PIL import Image, ImageGrab
import StringIO


class Screenshot(object):

    @staticmethod
    def take(image_size=()):
        """
        :param image_size: a tuple contains the (width,height) of the image, if it remains
        empty the size will be the screen size.
        :return: a PIL.ImageGrab object of the screen shot.
        """
        image = ImageGrab.grab()
        if image_size:
            return image
        return image.resize(image_size, Image.ANTIALIAS)

    def get_screenshot_data(self, image_resize=()):
        """
        :param image_resize: a tuple contains the (width,height) of the image, if it remains
        empty the size will be the screen size.
        :return: the raw data of your screen shot image.
        """
        image = self.take(image_resize)
        output = StringIO.StringIO()
        image.save(output, format="JPEG", quality=95)
        image_data = output.getvalue()
        return image_data
