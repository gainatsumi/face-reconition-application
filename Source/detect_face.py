import cv2
import numpy as np
from PIL import Image

class detect_face():
    def __init__(self):
        self.model_yunet = cv2.FaceDetectorYN.create(model='Model/detet_face_model/face_detection_yunet_2022mar.onnx',
                    input_size=[128, 128],
                    config = "",
                    score_threshold=0.9,
                    nms_threshold=0.3,
                    top_k=5000,
                    backend_id= cv2.dnn.DNN_BACKEND_OPENCV,
                    target_id= cv2.dnn.DNN_TARGET_CPU)
        self.model_haarcascades = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    def crop_face(self, x, y, w, h, path):
        path = 'C:/Users/root/Pictures/Saved Pictures/test.jpg'
        image = cv2.imread(path)

        crop_img = image[y:y+h, x:x+w]

        img_resized = cv2.resize(crop_img, (96, 96), interpolation= cv2.INTER_LINEAR)
        return img_resized

    def detect(self, path):
        image = Image.open(path)
        image.save("Camera/image.jpg")
        path = "Camera/image.jpg"
        faces = []
        if (image.width > 1000 or image.height > 1000):
            faces = self.get_position_by_haarcascade(path)
        else:
            faces = self.get_position_by_yuna(path)
        return faces

    def get_position_by_haarcascade(self, path):
        image = cv2.imread(path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Detect faces in the image
        faces = self.model_haarcascades.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
        )
        return self.resize_face(faces)

    def get_position_by_yuna(self, path):
        faces = []
        image = cv2.imread(path)    
        h, w, _ = image.shape

        # Inference
        self.model_yunet.setInputSize(tuple([w, h]))
        results_1 = self.model_yunet.detect(image)
        results = results_1[1]
        for det in (results if results is not None else []):
            bbox = det[0:4].astype(np.int32)
            faces.append(bbox)
        faces = self.resize_face(faces)
        return faces
        
        
    def resize_face(self, faces):
        if(len(faces) > 0):
            for face in faces:
                x, y, w, h = face
                h_dived = int((h/4)/2)
                w_dived = int((w/4)/2)
                face[0] = x + w_dived
                face[1] = y + h_dived
                face[2] = w - w_dived
                face[3] = h - h_dived
            return faces
        else:
            return []


    
