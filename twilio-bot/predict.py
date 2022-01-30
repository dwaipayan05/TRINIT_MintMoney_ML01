import os
import cv2
import time
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from keras.models import model_from_json
from keras.preprocessing import image

covid_pred = ['Covid-19', 'Non Covid-19']
IMAGE_SIZE = 64

print(os.getcwd())
xception_model = '../cov-cnn/model_weights/Xception_Model.json'
xception_json = '../cov-cnn/model_weights/Xception_Model.json'

def resize_image(image, image_size):
    return cv2.resize(image.copy(), image_size, interpolation=cv2.INTER_AREA)


def read_image(filepath):
    return cv2.imread(filepath)


def resize_image(image, image_size):
    return cv2.resize(image.copy(), image_size, interpolation=cv2.INTER_AREA)


def clear_mediadir():
    media_dir = "/media"
    for f in os.listdir(media_dir):
        os.remove(os.path.join(media_dir, f))


def predict_COV():
    img_path = "/media/XRay.png"
    pred_arr = np.zeros((1, IMAGE_SIZE, IMAGE_SIZE, 3))

    im = read_image(img_path)
    if im is not None:
        pred_arr[0] = resize_image(im, (IMAGE_SIZE, IMAGE_SIZE))

    pred_arr = pred_arr/255
    print(type(pred_arr))
    xception_start = time.time()
    with open(xception_json, 'r') as xceptionjson:
        xceptionmodel = model_from_json(xceptionjson.read())
        xceptionmodel.load_weights(xception_model)
        label_xception = xceptionmodel.predict(pred_arr)
        idx_xception = np.argmax(label_xception[0])
        cf_score_xception = np.argmax(label_xception[1])

    print('Prediction (Xception): ', covid_pred[idx_xception])
    print('Confidence Score (Xception) : ', cf_score_xception)
    clear_mediadir()
    return (covid_pred[idx_xception], cf_score_xception)

if __name__ == "__main__":
    predict_COV()