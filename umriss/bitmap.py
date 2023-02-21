from nptyping import NDArray, Shape, UInt8
import cv2 as cv


GrayPixels = NDArray[Shape['* height, * width'], UInt8]


class Bitmap:
    """
    Represents a grayscale bitmap image.
    """
    def __init__(self, image_file: str):
        self.pixels: GrayPixels = cv.imread(image_file, cv.IMREAD_GRAYSCALE)
        self.height, self.width = self.pixels.shape
