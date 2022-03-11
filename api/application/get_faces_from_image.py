import numpy as np
from api.insightface.src.common import face_preprocess
from mtcnn.mtcnn import MTCNN
import cv2
import os
import sys
import datetime
from api.application import constants

# sys.path.append('../insightface/deploy')
# sys.path.append('../insightface/src/common')
sys.path.append(os.path.join(constants.ROOT_DIR, 'insightface', 'deploy'))
sys.path.append(os.path.join(constants.ROOT_DIR,
                'insightface', 'src', 'common'))


def get_faces_from_image(imagePath, nameFolder):
    """
        Get faces in new image and store list faces in personal folder
        :param imagePath: path of new image
        :param nameFolder: name folder to store list faces
        :return [str]
    """
    outPath = constants.FACE_REGISTER_FOR_TRAIN_PATH + '/' + nameFolder

    # Detector = mtcnn_detector
    detector = MTCNN()

    # Read Imgae
    frame = cv2.imread(imagePath)

    faces = 0

    bboxes = detector.detect_faces(frame)

    # image list return
    images = []
    area = 0
    face = 0
    filename_output = ''

    if len(bboxes) != 0:
        # Get only the biggest face
        for bboxe in bboxes:
            bbox = bboxe["box"]
            bbox = np.array([bbox[0], bbox[1], bbox[0] +
                            bbox[2], bbox[1] + bbox[3]])

            landmarks = bboxe["keypoints"]

            # convert to face_preprocess.preprocess input
            landmarks = np.array(
                [landmarks["left_eye"][0], landmarks["right_eye"][0], landmarks["nose"][0], landmarks["mouth_left"][0],
                 landmarks["mouth_right"][0],
                 landmarks["left_eye"][1], landmarks["right_eye"][1], landmarks["nose"][1], landmarks["mouth_left"][1],
                 landmarks["mouth_right"][1]])
            landmarks = landmarks.reshape((2, 5)).T
            nimg = face_preprocess.preprocess(
                frame, bbox, landmarks, image_size='112,112')
            if not (os.path.exists(outPath)):
                os.makedirs(outPath)

            timestamp = int(datetime.datetime.now().timestamp())

            # cv2.imwrite(os.path.join(outPath, "{}.jpg".format(faces+1)), nimg)
            cv2.rectangle(frame, (bbox[0], bbox[1]),
                          (bbox[2], bbox[3]), (255, 0, 0), 2)

            if area < (bbox[0] - bbox[2]) * (bbox[1] - bbox[3]):
                area = (bbox[0] - bbox[2]) * (bbox[1] - bbox[3])
                face = nimg
                filename_output = "{}.jpg".format(timestamp)
                # draw rectangle to face detect in image input file
                cv2.imwrite(imagePath, frame)

        cv2.imwrite(os.path.join(outPath, filename_output), face)
        images.append(filename_output)
    return images
