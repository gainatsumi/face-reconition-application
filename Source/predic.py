#thêm 1 số thử viện cần thiết
from tensorflow import keras
import tensorflow as tf
import numpy as np

#lấy model đã training
class predic():
    def __init__(self):
        self.model = keras.models.load_model('model/predic_model')

    #hàm predic_function: dùng để dự đoán và trả lại kểt quả
    def predic_function(self, img):
        #chuyển dạng ảnh sang dạng array để pù hợp model
        input_arr = keras.utils.img_to_array(img)
        # Convert single image to a batch.
        input_arr = np.array([input_arr])  
        #lấy array được dự đoán
        a = self.model.predict(input_arr)
        return a

    #hàm to_class: chuyển kết quả từ dự đoán sang các nhãn 
    def to_class(self, img):
        predic = self.predic_function(img)
        #các class
        class_labels = ['Female','Male']

        # Convert array sự đoán sang class labels

        if (predic[0][0] < 0 and predic[0][1] < 0):
            return "unknow"
        else:
            #np.argmax: trả về giá trị lớn nhất trên 1 trục (axis = 1)
            predicted_indices = np.argmax(predic, axis=1) 
            predicted_classes = [class_labels[i] for i in predicted_indices]
            return predicted_classes