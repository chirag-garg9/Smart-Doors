import torch  # Import PyTorch for deep learning operations
import torchvision.transforms as transforms  # Import image transformations
from PIL import Image  # Import Python Imaging Library for image processing
from facenet_pytorch import MTCNN, InceptionResnetV1  # Import face detection and mode

# Extracting face from the image.
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
    mtcnn = MTCNN(image_size=required_size)  # Initialize MTCNN for face detection

    # Detect faces in the image
    boxes, _ = mtcnn.detect(image)  # Get bounding boxes of detected faces

    # Extract the first detected face
    if boxes is not None and len(boxes) > 0:
        box = boxes[0]  # Access the first detected face
        x1, y1, width, height = box  # Extract bounding box coordinates
        x2, y2 = x1 + width, y1 + height  # Calculate bottom-right coordinates
        face = image.crop((x1, y1, x2, y2))  # Crop the face region from the image
       # print(face.size)       
        face=face.resize((224,224))
        # Convert face to a PyTorch tensor
        face_tensor = transforms.ToTensor()(face).unsqueeze(0)  # Add a batch dimension
        return face_tensor  # Return the face tensor
    else:
        return None  # Return None if no faces are detected

# Load the photo and extract the face
face_tensor = extract_face(path=r"C:\Users\hp\Desktop\phuto.jpg")

# Create the VGGFace2 model (InceptionResnetV1)
model = InceptionResnetV1(pretrained='vggface2').eval()  # Load pretrained model and set to evaluation mode

# Perform prediction
with torch.no_grad():  # Disable gradient calculation
    
    #get embeddings function.
 def getembeddings(embeddings):
     embeddings = model(face_tensor)  # Generate face embeddings
     return (embeddings)
# Compare embeddings with other face embeddings for verification (replace with your comparison logic)
# ...
