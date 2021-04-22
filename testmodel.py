import numpy as np
import pickle
import cv2
from keras.models import load_model
import keras.models
from keras.preprocessing.image import img_to_array

Categories = ["Eggplant Healthy", 
              "Pepper Bell Bacterial Spot",
              "Pepper Bell Healthy", 
              "Pepper Chili Healthy", 
              "Potato Early Blight", 
              "Potato Healthy",
              "Potato Late Blight", 
              "Tomato Bacterial Spot", 
              "Tomato Early Blight",
              "Tomato Healthy",
              "Tomato Late Blight",
              "Tomato Target Spot"]

width = 256
height = 256
depth = 3

imagefilepath = "D:/Res/data testset/Eggplant Healthy/1.jpg"
model = keras.models.load_model("diseasedetectmodel1.h5")
default_image_size = tuple((256, 256))


def convert_image_to_array(image_dir):
    try:
        image = cv2.imread(image_dir)
        if image is not None:
            image = cv2.resize(image, default_image_size)
            return img_to_array(image)
        else:
            return np.array([])
    except Exception as e:
        print(f"Error : {e}")
        return None

for x in range(1, 26):
    im = convert_image_to_array("D:/Res/data testset/Eggplant Healthy/"+ str(x) +".jpg")
    np_image_li = np.array(im, dtype=np.float16) / 225.0
    npp_image = np.expand_dims(np_image_li, axis=0)
    result = model.predict(npp_image)
    print(result)
    print("Image "+ str(x) +" : "+Categories[np.argmax(result[0])])
