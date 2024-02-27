import torch  
import torchvision.transforms as transforms 
from deepface import DeepFace
from PIL import Image  
from facenet_pytorch import MTCNN, InceptionResnetV1 
from tqdm import tqdm 
from deepface.commons import functions
import pandas as pd
from pymongo import MongoClient
 #Extracts a single face from a given photograph.
def extract_face(path=r"c:\Users\hp\Desktop\phuto.jpg", required_size=(224, 224)):
    """Extracts a single face from a given photograph.

    Args:
        filename (str): The path to the image file.
        required_size (tuple, optional): The required size of the face image. Defaults to (224, 224).

    Returns:
        torch.Tensor: The extracted and resized face tensor.
    """
   

    # Load image from file
    image = Image.open(path)

    # Create MTCNN detector
    mtcnn = MTCNN(image_size=required_size)  

    # Detect faces in the image and creates bounding boxes.
    boxes, _ = mtcnn.detect(image)  

    # Extract the first detected face
    if boxes is not None and len(boxes) > 0:
        box = boxes[0]  
        x1, y1, width, height = box  
        x2, y2 = x1 + width, y1 + height 
        face = image.crop((x1, y1, x2, y2))  
       # print(face.size)       
        face=face.resize((224,224))
        # Convert face to a PyTorch tensor
        face_tensor = transforms.ToTensor()(face).unsqueeze(0)  
        return face_tensor  
    else:
        return None  

# Load the photo and extract the face
face_tensor = extract_face(path=r"C:\Users\hp\Desktop\phuto.jpg")

# Create the VGGFace2 model (InceptionResnetV1)
model = InceptionResnetV1(pretrained='vggface2').eval()  # Load pretrained model and set to evaluation mode

# Perform prediction
with torch.no_grad():  
    embeddings = model(face_tensor)  
    print (embeddings)
# Compare embeddings with other face embeddings for verification (replace with your comparison logic)
# ...
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
