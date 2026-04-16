import cv2
import numpy as np

# --- Пути к файлам ---
CLASSES_FILE = "10-2_coco.names"
IMAGE_PATH = "10-4_test_image.jpg"      # выберите ваше изображение из COCO test2017
CONFIG = "10-3_yolov4.cfg"
WEIGHTS = "yolov4.weights"

CONFIDENCE_THRESHOLD = 0.5         # порог уверенности (пока можно 0.5)
NMS_THRESHOLD = 0.4                # Non‑maximum suppression

# --- Загрузка классов ---
with open(CLASSES_FILE, "r") as f:
    classes = [line.strip() for line in f.readlines()]

# --- Подготовка нейросети ---
net = cv2.dnn.readNetFromDarknet(CONFIG, WEIGHTS)

# Включаем GPU (опционально, если есть CUDA):
# net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
# net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

layer_names = net.getLayerNames()
out_layer_names = net.getUnconnectedOutLayers()
output_layers = [layer_names[i - 1] for i in out_layer_names]

# --- Загрузка изображения ---
image = cv2.imread(IMAGE_PATH)
height, width = image.shape[:2]

# --- Подготовка blob (размер 416×416, кратен 32) ---
blob = cv2.dnn.blobFromImage(
    image,
    scalefactor=1./255.,
    size=(416, 416),     # или 512, 608, 672 и т.п., главное кратно 32
    swapRB=True,
    crop=False
)
net.setInput(blob)

# --- Прогноз ---
outs = net.forward(output_layers)

# --- Разбор результатов ---
boxes = []
class_ids = []
confidences = []

for out in outs:
    for detection in out:
        scores = detection[5:]
        class_id = np.argmax(scores)
        confidence = scores[class_id]

        if confidence > CONFIDENCE_THRESHOLD:
            # Обратим нормализацию координат к размерам исходного изображения
            center_x = int(detection[0] * width)
            center_y = int(detection[1] * height)
            w = int(detection[2] * width)
            h = int(detection[3] * height)

            x = int(center_x - w / 2)
            y = int(center_y - h / 2)

            boxes.append([x, y, w, h])
            class_ids.append(class_id)
            confidences.append(float(confidence))

# --- Non‑maximum suppression ---
indices = cv2.dnn.NMSBoxes(boxes, confidences, CONFIDENCE_THRESHOLD, NMS_THRESHOLD)

# --- Отображение результатов ---
if len(indices) > 0:
    for i in indices:
        box = boxes[i]
        x, y, w, h = box
        class_id = class_ids[i]
        label = f"{classes[class_id]} ({confidences[i]:.2f})"
        color = (0, 255, 0)

        cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
        cv2.putText(image, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

cv2.imshow("Detected Objects", image)
cv2.waitKey(0)
cv2.destroyAllWindows()