import cv2
import numpy as np
from qr_parser import QrCodeParser

if __name__ == '__main__':
    """
        Executes QR Code parser
    """

    # Please, replace with your qr code
    image_path = r'images/qr3.jpg'
    parser = QrCodeParser(image_path=image_path)
    parser.parse_image()
    parser.get_cords()
