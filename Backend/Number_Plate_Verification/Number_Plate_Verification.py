from ultralytics import YOLO
import cv2
from Util import *
import numpy as np
import os

# The NumPlateOperations class performs license plate detection, processing, and number extraction
# from video frames, and provides a function to verify the number plate.
class NumPlateOperations:
    def __init__(self):
        self.license_plate_detector = YOLO('./best.pt')
        self.results = []

    def read_frames(self,images):
        """
        Read frames from a video capture object, detect license plates,
        and process each license plate to extract the license plate number.

        Args:
            cap: Video capture object.

        Returns:
            list: List of results containing license plate numbers and scores.
        """
        for image in os.listdir(images):
            # Retrieve image data from GridFS
            frame  = cv2.imread(image)
            license_plates = self.license_plate_detector(frame)[0]
            for license_plate in license_plates.boxes.data.tolist():
                x1, y1, x2, y2, score, class_id = license_plate

                # Crop license plate
                license_plate_crop = frame[int(y1):int(y2), int(x1):int(x2), :]

                # Process license plate
                license_plate_crop_gray = cv2.cvtColor(license_plate_crop, cv2.COLOR_BGR2GRAY)
                _, license_plate_crop_thresh = cv2.threshold(license_plate_crop_gray, 64, 255, cv2.THRESH_BINARY_INV)

                # Read license plate number
                license_plate_text, license_plate_text_score = self.read_license_plate(license_plate_crop_thresh)

                if license_plate_text is not None:
                    self.results.append([license_plate_text, license_plate_text_score])

        return self.results

    def verify_number_plate (self,images,Number_plates):
        """
        The function "verify_number_plate" reads frames, calculates top k scores, and performs a search
        based on the results.
        :return: the result of the search function.
        """
        results = self.read_frames(images)
        self.results = []
        results = top_k_scores(results)
        return search(results,Number_plates)
               