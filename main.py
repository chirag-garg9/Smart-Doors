from ultralytics import YOLO
import cv2
import util
from util import get_car, read_license_plate, write_csv

results = []

# load models
coco_model = YOLO('yolov8n.pt')
license_plate_detector = YOLO('./best.pt')

# load video
cap = cv2.VideoCapture('./sample.mp4')

# read frames
frame_nmr = -1
ret = True
while ret:
    frame_nmr += 1
    ret, frame = cap.read()
    if ret:
        # results[frame_nmr] = {}

        # detect license plates
        license_plates = license_plate_detector(frame)[0]
        for license_plate in license_plates.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = license_plate

            # crop license plate
            license_plate_crop = frame[int(y1):int(y2), int(x1): int(x2), :]

            # process license plate
            license_plate_crop_gray = cv2.cvtColor(license_plate_crop, cv2.COLOR_BGR2GRAY)
            _, license_plate_crop_thresh = cv2.threshold(license_plate_crop_gray, 64, 255, cv2.THRESH_BINARY_INV)

            # read license plate number
            license_plate_text, license_plate_text_score = read_license_plate(license_plate_crop_thresh)

            if license_plate_text is not None:
                results.append([license_plate_text,license_plate_text_score])
                

# write results
write_csv(results, './test.csv')