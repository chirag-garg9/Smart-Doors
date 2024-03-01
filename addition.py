import torch  
import torchvision.transforms as transforms 
from deepface import DeepFace
from PIL import Image  
from facenet_pytorch import MTCNN, InceptionResnetV1 
from tqdm import tqdm 
from deepface.commons import functions
import pandas as pd
from pymongo import MongoClient
from Backend.Number_Plate_identification.util import *
 #Connecting to mongoDb
connection = "mongodb+srv://..."
client = MongoClient(connection)
database = 'deepface'; collection = 'deepface'
db = client[database]
#loading image. 
facial_img_paths = []

instances = []
 
for i in tqdm(range(0, len(facial_img_paths))):
    facial_img_path = facial_img_paths[i]    
    embedding = DeepFace.represent(img_path = facial_img_path, model_name = "Facenet")[0]["embedding"]
     
    instance = []
    instance.append(facial_img_path)
    instance.append(embedding)
    instances.append(instance)
#preprocessing
df = pd.DataFrame(instances, columns = ["img_name", "embedding"])
df.head()
    #Storing embeddings in mongoDb
for index, instance in tqdm(df.iterrows(), total = df.shape[0]):
    db[collection].insert_one({"img_path": instance["img_name"], "embedding" : instance["embedding"].tolist()})
    #Target face
    target_img_path = "target.jpg"
target_img = DeepFace.extract_faces(img_path = target_img_path)[0]["face"]
target_embedding = DeepFace.rerpresent(img_path = target_img_path, model_name = "Facenet")[0]["embedding"]
    #some quesries.
documents = db[collection].find()
 
for document in documents:
    print(document["img_path"], document["embedding"])
    query = db[collection].aggregate( [
   {
       "$addFields": { 
           "target_embedding": target_embedding
       }
   }
] )
