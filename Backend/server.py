from flask import Flask, request
import cv2
import numpy as np
from pymongo import MongoClient
from Number_Plate_Verification.number_plate_verification import NumPlateOperations
from gridfs import GridFS
import multiprocessing

proccesser = Flask(__name__)

class operation():
    def __init__(self):
        self.number_plate_verifier = NumPlateOperations()
        # self.face_recognizer = FaceRecognizer()
        # Connect to MongoDB
        self.client = MongoClient('mongodb://localhost:27017/')
        self.m = 0


Operatios = operation()
@proccesser.route("/recieve_data",methods=["Post","Get"])
def upload():
    # Check if the request contains binary data or a string
    if request.content_type.startswith('image'):
        # Binary data: Read the raw binary data from the request body
        image_binary = request.data
        db = Operatios.client['test_database']
        fs = GridFS(db)
        image_id = fs.put(image_binary, filename=f'image{Operatios.m}.jpg')
        
    else:
        def process_method(method,*args):
            return method(*args)
        num_processes = multiprocessing.cpu_count()
        pool = multiprocessing.Pool(processes=num_processes)
        
        # Map the methods to the pool
        results = pool.map(process_method, [(Operatios.number_plate_verifier.verify_number_plate,db,fs), Operatios.face_recognizer])
        
        # Close the pool
        pool.close()
        pool.join()
        
        # Compute the OR of the results
        final_result = any(results)
        return final_result


if __name__ == '__main__':
    proccesser.run(debug=True)
    