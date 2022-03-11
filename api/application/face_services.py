from api.application.get_faces_from_image import get_faces_from_image
from api.application.train_softmax import train
from api.application.recognizer_image import recognizer_image
flag = "recognizer"

if flag == "resgiter":
    # resgiter face for person
    get_faces_from_image(imagePath="../datasets/test/001.jpg", nameFolder="binh")
elif flag == "train":
    # Retrain model
    status = train()
    print(status)
elif flag == "recognizer":
    # recognizer person in image
    result = recognizer_image(pathImageIn="../datasets/test/002.jpg", pathImageOut="../datasets/test/img_test_2.jpg")
    print(result)

