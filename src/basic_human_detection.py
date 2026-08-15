import cv2
from ultralytics import YOLO

model = YOLO("yolo26n.pt")

image = cv2.imread("datasets/WiderPerson/Images/000042.jpg")

results = model(image, classes=[0], conf=0.5, verbose=False)

annotated = results[0].plot()

cv2.imshow("Basic Human Detecton", annotated)
cv2.waitKey(0)
cv2.destroyAllWindows()
