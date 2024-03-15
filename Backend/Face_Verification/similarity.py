import argparse
import os
import numpy as np
from embeddings import get_embedding


def similarity(images,pre_embedding):
    embeddings = []
    for image in os.listdir(images):
        embeddings.append(get_embedding(os.path.join(images,image),r'C:\Users\Aditya\OneDrive\Desktop\ROBO\Smart-Doors\Backend\Face_Verification\Face-Recognition-with-ArcFace\backbone_ir50_ms1m_epoch120.pth'))
    cos_similarity = np.dot(np.array(embeddings), np.array(embeddings).T)
    max_similarity = 0
    cos_similarity = list(cos_similarity)
    for i in range(len(cos_similarity)):
        for j in range(len(cos_similarity[i])):
            max_similarity = max(max_similarity,cos_similarity[i][j])
    if(max_similarity>=0.7): return True
    else : return False

# print(similarity(r'C:\Users\Aditya\OneDrive\Desktop\ROBO\Smart-Doors\Backend\Face_Verification\testexamples'))