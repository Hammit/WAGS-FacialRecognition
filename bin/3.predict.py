#!/usr/bin/env python

import argparse
import cv2
import cv2.face as face

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Recognize an image against a trained data set (currently EigenFaceRecognizer)')
    parser.add_argument('training_filename', help='The training data generated by 2.train.py')
    parser.add_argument('image_filename', help='The image containing the face to recognize')
    parser.add_argument('-n', '--num-components', type=int, default=10, help='Number of components used in training (default: 10)')
    parser.add_argument('-t', '--threshold', type=float, default=12.5, help='Confidence threshold (default: 12.5)')

    args = parser.parse_args()

    model = face.createEigenFaceRecognizer(args.num_components, args.threshold)
    model.load(args.training_filename)

    # Load the image to recognize. Must be greyscale
    predict_img = cv2.imread(args.image_filename, cv2.IMREAD_GRAYSCALE)

    label, confidence = model.predict(predict_img)

    print("The predicted label was: %d" % label)
    print("The confidence was: %f" % confidence)
