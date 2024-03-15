import cv2
import numpy as np
import torch
import torch.nn.functional as F
from backbone import Backbone
from torchvision import transforms
import os
from facenet_pytorch import MTCNN

mtcnn = MTCNN(keep_all=True, device='cpu')

def preprocess_image(img_path):
    try:
        img = cv2.imread(img_path) # Example using OpenCV
        print(img.shape)
        boxes, probs = mtcnn.detect(img)
        if img is None:
            raise Exception("Failed to load image")
        
        # Ensure the image has exactly 3 channels (RGB)
        if img.shape[2] != 3:
            raise Exception("Image does not have 3 channels (RGB)")
        
        # Crop and resize face region
        if boxes is not None:
            x1, y1, x2, y2 = boxes[0].astype(int)
            face = img[y1:y2, x1:x2]
            face = cv2.resize(face, (112, 112))  # Resize to the input size expected by the backbone
            img = face
        
        # Convert image to float32
        img = img.astype(np.float32)  
        # Normalize image
        img /= 255.0
        return img  # Return preprocessed image
    except Exception as e:
        print(f"Error preprocessing image: {e}")
        return None

def get_embedding(image_path, model_root, input_size=[112, 112], embedding_size=512):

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    # check model path
    assert os.path.exists(model_root)
    print(f"Model root: {model_root}")

    # define image preprocessing
    transform = transforms.Compose(
            [transforms.ToTensor()]
    )

    # load image
    img = preprocess_image(image_path)
    # print(img.shape)
    # cv2.imshow("image",img)
    image = transform(img)  # avoid modifying original image
    image = image.unsqueeze(0).to('cpu')

    # load backbone weigths from a checkpoint
    backbone = Backbone(input_size)
    backbone.load_state_dict(torch.load(model_root, map_location=torch.device("cpu")))
    backbone.to(device)
    backbone.eval()

    # get embedding
    with torch.no_grad():        
        embedding = F.normalize(backbone(image)).cpu()

    return embedding.numpy()[0]  # Extract first element from batch

# The `get_embedding` function is being called with the path to an image file (`known.jpg`) and the
# path to a pre-trained model checkpoint file (`backbone_ir50_ms1m_epoch120.pth`).
# get_embedding(r'C:\Users\Aditya\OneDrive\Desktop\ROBO\Smart-Doors\Backend\Face_Verification\Face-Recognition-with-ArcFace\known.jpg', r'C:\Users\Aditya\OneDrive\Desktop\ROBO\Smart-Doors\Backend\Face_Verification\Face-Recognition-with-ArcFace\backbone_ir50_ms1m_epoch120.pth')