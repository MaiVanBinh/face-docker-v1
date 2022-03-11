import os
import time

from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import KFold
import matplotlib.pyplot as plt
from api.application.softmax import SoftMax
import numpy as np
import pickle
from api.application import constants
from api.application.faces_embedding import faces_embedding


def train(model_folder):
    # faces_embedding
    faces_embedding(model_folder)

    # config = {
    #     'embeddings': constants.FACE_DATA_VECTOR_PATH,
    #     'model': constants.FACE_MODEL_PATH,
    #     'le': constants.FACE_DATA_LABEL_PATH,
    #     "result_image": constants.TRAIN_ACC_LOSS_PATH
    # }

    embeddings_path = os.path.join(constants.ROOT_DIR, 'outputs', model_folder, constants.FACE_DATA_VECTOR_NAME)
    model_path = os.path.join(constants.ROOT_DIR, 'outputs', model_folder, constants.FACE_MODEL_NAME)
    le_path = os.path.join(constants.ROOT_DIR, 'outputs', model_folder, constants.FACE_DATA_LABEL_NAME)

    config = {
        'embeddings': embeddings_path,
        'model': model_path,
        'le': le_path,
        "result_image": constants.TRAIN_ACC_LOSS_PATH
    }

    # Load the face embeddings
    data = pickle.loads(open(config['embeddings'], "rb").read())

    # Encode the labels
    le = LabelEncoder()
    labels = le.fit_transform(data["names"])
    num_classes = len(np.unique(labels))
    labels = labels.reshape(-1, 1)
    one_hot_encoder = OneHotEncoder()
    labels = one_hot_encoder.fit_transform(labels).toarray()

    embeddings = np.array(data["embeddings"])

    # Initialize Softmax training model arguments
    BATCH_SIZE = 32
    EPOCHS = 20
    input_shape = embeddings.shape[1]

    # Build sofmax classifier
    softmax = SoftMax(input_shape=(input_shape,), num_classes=num_classes)
    model = softmax.build()

    # Create KFold
    cv = KFold(n_splits=5, random_state=42, shuffle=True)
    history = {'acc': [], 'val_acc': [], 'loss': [], 'val_loss': []}
    # Train
    for train_idx, valid_idx in cv.split(embeddings):
        X_train, X_val, y_train, y_val = embeddings[train_idx], embeddings[
            valid_idx], labels[train_idx], labels[valid_idx]
        his = model.fit(X_train, y_train,
                        batch_size=BATCH_SIZE,
                        epochs=EPOCHS,
                        verbose=1,
                        validation_data=(X_val, y_val))
        # print(his.history['accuracy'])

        history['acc'] += his.history['accuracy']
        history['val_acc'] += his.history['val_accuracy']
        history['loss'] += his.history['loss']
        history['val_loss'] += his.history['val_loss']

    # write the face recognition model to output
    model.save(config['model'])
    f = open(config["le"], "wb")
    f.write(pickle.dumps(le))
    f.close()

    # LocNguyen close because write plot will crash app
    # # Plot
    # plt.figure(1)
    # # Summary history for accuracy
    # plt.subplot(211)
    # plt.plot(history['acc'])
    # plt.plot(history['val_acc'])
    # plt.title('model accuracy')
    # plt.ylabel('accuracy')
    # plt.xlabel('epoch')
    # plt.legend(['train', 'test'], loc='upper left')
    #
    # # Summary history for loss
    # plt.subplot(212)
    # plt.plot(history['loss'])
    # plt.plot(history['val_loss'])
    # plt.title('model loss')
    # plt.ylabel('loss')
    # plt.xlabel('epochs')
    # plt.legend(['train', 'test'], loc='upper left')
    # plt.savefig(config['result_image'])

    print("Train success")

    return "Train success"
