import cv2
from ultralytics import YOLO

model = YOLO("yolo26n.pt")

video = cv2.VideoCapture("archive/Videos/Videos/fall/YOUTUBE_YouTubeCCTV001_fall_51.mp4")

width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

cv2.namedWindow("Basic Human Detection + Tracking", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Basic Human Detection + Tracking", width // 2, height // 2)

while True:
    ret, frame = video.read()
    if not ret:
        break

    results = model.track(
        frame,
        classes=[0],
        conf=0.5,
        persist=True,
        tracker="custom_botsort.yaml",
        verbose=False,
    )

    annotated = results[0].plot()

    cv2.imshow("Basic Human Detection + Tracking", annotated)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

video.release()
cv2.destroyAllWindows()
