import cv2
import numpy as np
import glob
import os

LAST_NAME = "Trifonov"

img = cv2.imread("9-3_image.png")
if img is not None:
    scaled = cv2.resize(img, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)  # [web:1]
    scaled = cv2.resize(scaled, (img.shape[1], img.shape[0]))

    blur3 = cv2.GaussianBlur(img, (3, 3), 0)
    blur9 = cv2.GaussianBlur(img, (9, 9), 0)  # [web:4][web:52]

    top = np.hstack([img, scaled])
    bottom = np.hstack([blur3, blur9])
    collage = np.vstack([top, bottom])

    h, w = img.shape[:2]
    font = cv2.FONT_HERSHEY_SIMPLEX
    red = (0, 0, 255)

    cv2.putText(collage, "Original", (20, 40), font, 1, red, 2)
    cv2.putText(collage, "Scaled 0.5x", (w + 20, 40), font, 1, red, 2)
    cv2.putText(collage, "Blur 3x3", (20, h + 40), font, 1, red, 2)
    cv2.putText(collage, "Blur 9x9", (w + 20, h + 40), font, 1, red, 2)

    cv2.putText(
        collage,
        f"Scaling + Blurring, {LAST_NAME}",
        (20, collage.shape[0] - 20),
        font,
        1,
        (255, 0, 0),
        2,
    )

    cv2.imshow("Task 1: Scaling and Blurring", collage)
    cv2.imwrite("9-4_task1_result.png", collage)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if os.path.exists("9-2_haarcascade_frontalface_default.xml"):
    face_cascade = cv2.CascadeClassifier("9-2_haarcascade_frontalface_default.xml")  # [web:45][web:48]

    face_images = glob.glob("face*.png")

    for path in face_images:
        img = cv2.imread(path)
        if img is None:
            continue

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(60, 60),
        )

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(
                img,
                LAST_NAME,
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 0, 0),
                2,
            )

        cv2.imshow(f"Task 2: {os.path.basename(path)}", img)
        out_name = os.path.splitext(path)[0] + "_faces.png"
        cv2.imwrite(out_name, img)
        key = cv2.waitKey(0)
        if key == 27:
            break

    cv2.destroyAllWindows()