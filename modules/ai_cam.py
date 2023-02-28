# %%
from transformers import pipeline, ImageClassificationPipeline
import torch
from time import time
# %%
import cv2
from PIL import Image
ai: ImageClassificationPipeline = pipeline(
    "image-classification", model="Rajaram1996/FacialEmoRecog")
# %%
# ai.device = torch.device("mps")
# ai.model.to('mps')

webcam = cv2.VideoCapture(0)

# if not webcam.isOpened():
#     print("Could not open webcam")
#     exit()
def cam():
    result = ["emotion not detected"]
    if webcam.isOpened():
        print("capturing...")
        status, frame = webcam.read()
        if status:
            result = ai(Image.fromarray(frame))
        result = [f"{s['label']}: {s['score']*100:5.1f}%" for s in result]
    return result

def free_cam():
    webcam.releasez