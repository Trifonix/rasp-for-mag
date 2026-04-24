import cv2

WEIGHTS   = "yolov4.weights"
CONFIG    = "10-3_yolov4.cfg"
INPUT_IMG = "11-2_input.jpg"
OUTPUT_IMG = "11-3_prediction.jpg"


CLASSES = [
    "person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
    "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
    "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack",
    "umbrella", "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball",
    "kite", "baseball bat", "baseball glove", "skateboard", "surfboard", "tennis racket",
    "bottle", "wine glass", "cup", "fork", "knife", "spoon", "bowl", "banana", "apple",
    "sandwich", "orange", "broccoli", "carrot", "hot dog", "pizza", "donut", "cake",
    "chair", "sofa", "potted plant", "bed", "dining table", "toilet", "tvmonitor", "laptop",
    "mouse", "remote", "keyboard", "cell phone", "microwave", "oven", "toaster", "sink",
    "refrigerator", "book", "clock", "vase", "scissors", "teddy bear", "hair drier",
    "toothbrush"
]


def detect_coco_yolov4():
    try:
        net = cv2.dnn.readNetFromDarknet(CONFIG, WEIGHTS)
    except Exception as e:
        print("Ошибка загрузки модели:", repr(e))
        return
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)

    model = cv2.dnn_DetectionModel(net)
    model.setInputParams(size=(416, 416), scale=1/255, swapRB=True)

    img = cv2.imread(INPUT_IMG)
    if img is None:
        print("Не удалось загрузить изображение:", INPUT_IMG)
        return

    class_ids, confidences, boxes = model.detect(
        img,
        confThreshold=0.3,
        nmsThreshold=0.4
    )

    print("Обнаружено объектов:", len(class_ids))
    for i, (class_id, score, box) in enumerate(zip(class_ids, confidences, boxes)):
        x, y, w, h = box
        label = f"{CLASSES[class_id]}: {score:.2f}"
        print(f"  {i:2d}) {label} -> box=(x:{x}, y:{y}, w:{w}, h:{h})")

        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(img, label, (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    if len(class_ids) == 0:
        print("Модель НЕ обнаружила объектов на изображении с порогом 0.3.")

    cv2.imwrite(OUTPUT_IMG, img)
    print(f"Результат сохранён: {OUTPUT_IMG}")

    cv2.imshow("YOLOv4 (COCO)", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    detect_coco_yolov4()
