# preprocessing.py
import cv2, os   # OpenCV for Computer Vision
import pytesseract
import numpy as np
from matplotlib import pyplot as plt

class PreProcessingPhase:
    def __init__(self, data=None):
        self.data = data
        self.image_file = "./data/bill_sample.png"
        self.img = cv2.imread(self.image_file)
    
    # --------------------------------------------------------------------------
    # Standerd function for all computer matrix to identify Invoice/Form/ID Card 
    # --------------------------------------------------------------------------
    def compute_metrics(gray):
        lap_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        contrast = gray.std()
        edges = cv2.Canny(gray, 50, 150)
        edge_density = edges.sum() / edges.size
        return lap_var, contrast, edge_density
  


