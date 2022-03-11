from api.application import constants
import os

import sys

# sys.path.append('../insightface/deploy')
# sys.path.append('../insightface/src/common')
sys.path.append(os.path.join(constants.ROOT_DIR, 'insightface', 'deploy'))
sys.path.append(os.path.join(constants.ROOT_DIR, 'insightface', 'src', 'common'))

import cv2
import pickle
# import face_model
from api.insightface.deploy import face_model
import numpy as np
from imutils import paths


def faces_embedding(model_folder):
    # args = {
    #     'model': constants.FACE_MODEL_CONFIGURATION,
    #     'image_size': constants.FACE_INPUT_IMAGE_SIZE,
    #     'ga_model': '',
    #     'threshold': 1.24,
    #     'det': 0,
    #     'dataset': constants.FACE_REGISTER_FOR_TRAIN_PATH,
    #     'embeddings': constants.FACE_DATA_VECTOR_PATH
    # }

    embeddings_path = os.path.join(constants.ROOT_DIR, 'outputs', model_folder, constants.FACE_DATA_VECTOR_NAME)

    args = {
        'model': constants.FACE_MODEL_CONFIGURATION,
        'image_size': constants.FACE_INPUT_IMAGE_SIZE,
        'ga_model': '',
        'threshold': 1.24,
        'det': 0,
        'dataset': constants.FACE_REGISTER_FOR_TRAIN_PATH,
        'embeddings': embeddings_path
    }

    # Grab the paths to the input images in our dataset
    # print("[INFO] quantifying faces...")
    imagePaths = list(paths.list_images(args['dataset']))

    # Initialize the faces embedder
    embedding_model = face_model.FaceModel(args)

    # Initialize our lists of extracted facial embeddings and corresponding people names
    knownEmbeddings = []
    knownNames = []

    # Initialize the total number of faces processed
    total = 0

    # Loop over the imagePaths
    for (i, imagePath) in enumerate(imagePaths):
        # extract the person name from the image path
        # print("[INFO] processing image {}/{}".format(i+1, len(imagePaths)))
        name = imagePath.split(os.path.sep)[-2]

        # load the image
        image = cv2.imread(imagePath)
        # convert face to RGB color
        nimg = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        nimg = np.transpose(nimg, (2, 0, 1))
        # Get the face embedding vector
        face_embedding = embedding_model.get_feature(nimg)

        # add the name of the person + corresponding face
        # embedding to their respective list
        knownNames.append(name)
        knownEmbeddings.append(face_embedding)
        total += 1

    # print(total, " faces embedded")

    # save to output
    data = {"embeddings": knownEmbeddings, "names": knownNames}
    f = open(args['embeddings'], "wb")
    f.write(pickle.dumps(data))
    f.close()
