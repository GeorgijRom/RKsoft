import cv2
import numpy as np


class QrCodeParser:
    """
    Class to parse and get QR Code coordinates
    """

    def __init__(self, **kwargs):
        # Path to the image
        self.image_path = str(kwargs.get("image_path"))
        self.close, self.image = None, None

    def parse_image(self):

        # Loads image
        self.image = cv2.imread(self.image_path)
        initial_image = self.image.copy()

        # grayscale with gaussian blur and threshold for the image
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (9,9), 0)
        thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

        # Morph close
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))

        # Gets distribution
        self.close = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)

    def get_cords(self):
        # Find contours and filter for QR code
        contours = cv2.findContours(self.close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = contours[0] if len(contours) == 2 else contours[1]

        # Looping through all values of contours
        for c in contours:
            # Getting length of the curve
            arc_vals = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.04 * arc_vals, True)

            # Getting cords and width, height
            x, y, w, h = cv2.boundingRect(approx)
            total_size = cv2.contourArea(c)
            ratio = w / float(h)

            # If QR is found
            if len(approx) == 4 and total_size > 1000 and (.85 < ratio < 1.3):
                cv2.rectangle(self.image, (x, y), (x + w, y + h), (36, 255, 12), 3)
                print(x, y, w, h)
                print("The coordinates of QR code are from (x, y):", x, y, "to (x, y):", x + w, y + h)

        # Shows highlighted QR code
        cv2.imshow('image', self.image)

        cv2.waitKey()