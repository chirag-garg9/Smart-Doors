from flask import Flask, request
import cv2
import os
import numpy as np
from Number_Plate_Verification.Number_Plate_Verification import NumPlateOperations
from Face_Verification.similarity import similarity
import multiprocessing
import pickle

path = os.getcwd()
os.makedirs(os.path.join(path,'./images'),exist_ok=True)
proccesser = Flask(__name__)
pre_embedding = []
Number_plates = pickle.dump()

class operation():
    def __init__(self):
        self.number_plate_verifier = NumPlateOperations()
        self.find_similarity = similarity
        self.m = 0

Operatios = operation()
@proccesser.route("/recieve_data",methods=["Post","Get"])
def upload():
    # Check if the request contains binary data or a string
    global image_buufer
    if(request.method == 'POST'):
        if request.headers['Content-Type'] == 'image/jpeg':
            image_buufer.extend(request.get_data())
            return "SUCCESS"
        else:
            try:
                print("Data Complete!")
                nparr = np.frombuffer(image_buufer, np.uint8)
                # Decode numpy array to image
                image_buufer = bytearray()
                img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                cv2.imwrite(img,os.path.join(path,f"images/Image{Operatios.m}.jpeg"))
                Operatios.m += 1
                if(Operatios.m==5):
                    Operatios.m = 0
                    def process_method(method,*args):
                        return method(*args)
                    num_processes = multiprocessing.cpu_count()
                    pool = multiprocessing.Pool(processes=num_processes)
                    path_abs = os.path.join(path,'images')
                    # Map the methods to the pool
                    results = pool.map(process_method, [(Operatios.number_plate_verifier.verify_number_plate,path_abs,Number_plates), (Operatios.find_similarity,path_abs,pre_embedding)])
                    # Close the pool
                    pool.close()
                    pool.join()
                    
                    # Compute the OR of the results
                    final_result = any(results)
                    return final_result
                if img.empty():
                    raise Exception("Error decoding data")
            except Exception as e:
                return "Image not decoded"
                        
      
    else: 
        return "<h1>No image</h1>"
        


if __name__ == '__main__':
    proccesser.run(debug=True)
    