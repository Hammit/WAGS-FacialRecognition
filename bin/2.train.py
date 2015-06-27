#!/usr/bin/env python
#
# Train a FaceRecognizer and save the training data for future predictions

import argparse
import csv
import numpy as np
import cv2
import cv2.face as face


# Take a csv file formatted with image_filename;label and load these images and labels
# into arrays for training
def load_csv(filename=None):
    cv_images = []
    labels = []
    with open(filename, 'rb') as csv_file:
        reader = csv.reader(csv_file, delimiter=';')
        for row in reader:
            image_filename, label = row
            image = cv2.imread(image_filename, cv2.IMREAD_GRAYSCALE)  # must load the image as greyscale
            cv_images.append(image)
            labels.append(int(label))

    # OpenCV requires a NumPy array of labels...Why? Just because
    labels = np.array(labels)

    return cv_images, labels


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Train a FaceRecognizer (currently EigenFaceRecognizer)')
    parser.add_argument('csv_filename', help='The CSV file of Images and Labels produced by 1.create-recognize-csv.py')
    parser.add_argument('training_filename', help='Save training data to this filename')
    parser.add_argument('-n', '--num-components', type=int, default=10, help='Number of components used in training (default: 10)')
    parser.add_argument('-t', '--threshold', type=float, default=12.5, help='Confidence threshold (default: 12.5)')

    args = parser.parse_args()

    print("Loading images from: " + args.csv_filename)
    images, labels = load_csv(args.csv_filename)

    print("Training {0} images".format(len(images)))
    model = face.createEigenFaceRecognizer(args.num_components, args.threshold)
    model.train(images, labels)

    print("Saving training data to: " + args.training_filename)
    model.save(args.training_filename)
