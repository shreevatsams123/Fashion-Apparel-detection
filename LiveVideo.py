# USAGE
# python classify.py --model fashion.model --labelbin mlb.pickle

# import the necessary packages
import warnings
print("Running Software...")
warnings.filterwarnings("ignore")
from keras.preprocessing.image import img_to_array
from keras.models import load_model
import numpy as np
import argparse
import imutils
import pickle
import cv2
import os

# construct the argument parse and parse the arguments
##ap = argparse.ArgumentParser()
##ap.add_argument("-m", "--model", required=True,
##	help="--fashion.model")
##ap.add_argument("-l", "--labelbin", required=True,
##	help="--mlb.pickle")
##ap.add_argument("-i", "--image", required=True,
##	help="path to input image")
##args = vars(ap.parse_args())
cap=cv2.VideoCapture(0)
print(cap)

while True :
        # load the image
        ret,image = cap.read()
        output = imutils.resize(image, width=400)
         
        # pre-process the image for classification
        image = cv2.resize(image, (96, 96))
        image = image.astype("float") / 255.0
        image = img_to_array(image)
        image = np.expand_dims(image, axis=0)

        # load the trained convolutional neural network and the multi-label
        # binarizer
        print("[INFO] loading network...")
        model = load_model('fashion.model')
        mlb = pickle.loads(open('mlb.pickle', "rb").read())

        # classify the input image then find the indexes of the two class
        # labels with the *largest* probability
        print("[INFO] classifying image...")
        proba = model.predict(image)[0]
        idxs = np.argsort(proba)[::-1][:2]

        # loop over the indexes of the high confidence class labels
        for (i, j) in enumerate(idxs):
                # build the label and draw the label on the image
                label = "{}: {:.2f}%".format(mlb.classes_[j], proba[j] * 100)
                cv2.putText(output, label, (10, (i * 30) + 25), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # show the probabilities for each of the individual labels
        for (label, p) in zip(mlb.classes_, proba):
                print("{}: {:.2f}%".format(label, p * 100))

        # show the output image
        cv2.imshow("Output", output)
        if cv2.waitKey(100) & 0xFF == ord('q'):
                break
