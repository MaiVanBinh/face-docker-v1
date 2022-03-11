import os
APP_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.join(os.path.dirname(APP_DIR))

# FACE_MODEL_PATH = '../outputs/my_model.h5'
# FACE_DATA_VECTOR_PATH = '../outputs/embeddings.pickle'
# FACE_DATA_LABEL_PATH = '../outputs/le.pickle'
# APPLICATION_OUTPUT_VIDEO_PATH = '../outputs/video/'
# FACE_MODEL_CONFIGURATION = '../insightface/models/model-y1-test2/model,0'
# FACE_INPUT_IMAGE_SIZE = '112,112'
# FACE_REGISTER_FOR_TRAIN_PATH = '../datasets/train'
# TRAIN_ACC_LOSS_PATH = "../outputs/accuracy_loss.png"

FACE_MODEL_PATH = os.path.join(ROOT_DIR, 'outputs', 'my_model.h5')
FACE_DATA_VECTOR_PATH = os.path.join(ROOT_DIR, 'outputs', 'embeddings.pickle')
FACE_DATA_LABEL_PATH = os.path.join(ROOT_DIR, 'outputs', 'le.pickle')
APPLICATION_OUTPUT_VIDEO_PATH = os.path.join(ROOT_DIR, 'outputs', 'video') + '/'
FACE_MODEL_CONFIGURATION = os.path.join(ROOT_DIR, 'insightface', 'models', 'model-y1-test2', 'model') + ',0'
FACE_INPUT_IMAGE_SIZE = '112,112'
FACE_REGISTER_FOR_TRAIN_PATH = os.path.join(ROOT_DIR, 'datasets', 'train')
TRAIN_ACC_LOSS_PATH = os.path.join(ROOT_DIR, "outputs", "accuracy_loss.png")

FACE_MODEL_NAME = 'my_model.h5'
FACE_DATA_VECTOR_NAME = 'embeddings.pickle'
FACE_DATA_LABEL_NAME = 'le.pickle'
