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

while webcam.isOpened():
    start = time()
    status, frame = webcam.read()
    if status:
        result = ai(Image.fromarray(frame))
        texts = [f"{s['label']:10s}: {s['score']*100:5.1f}%" for s in result] + \
            [f"fps: {1/(time()-start):.1f}fps"]
        print(texts)
        for i, text in enumerate(texts):
            frame = cv2.putText(frame, text.upper(), (50, 60*(i+1)),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
        # cv2.imshow("test", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

webcam.release()
cv2.destroyAllWindows()
