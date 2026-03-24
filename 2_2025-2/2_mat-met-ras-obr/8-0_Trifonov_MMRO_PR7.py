import cv2 as cv
import numpy as np
from http.server import BaseHTTPRequestHandler, HTTPServer
import base64
import threading
import webbrowser
import time

PORT = 8000

def encode_image(img):
    _, buffer = cv.imencode('.png', img)
    return base64.b64encode(buffer).decode('utf-8')

def process_image():
    logs = []

    img = cv.imread('8_1-coins.png')
    if img is None:
        raise Exception("Image not found: 8-1_coins.png")

    logs.append("✔ Изображение загружено")

    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    ret, thresh = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)
    logs.append(f"✔ Otsu threshold: {ret:.2f}")

    kernel = np.ones((3, 3), np.uint8)

    opening = cv.morphologyEx(thresh, cv.MORPH_OPEN, kernel, iterations=2)
    logs.append("✔ Удаление шума (opening)")

    sure_bg = cv.dilate(opening, kernel, iterations=3)
    logs.append("✔ Найден фон")

    dist_transform = cv.distanceTransform(opening, cv.DIST_L2, 5)
    ret, sure_fg = cv.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)
    logs.append("✔ Найден передний план")

    sure_fg = np.uint8(sure_fg)
    unknown = cv.subtract(sure_bg, sure_fg)
    logs.append("✔ Найдена неизвестная область")

    ret, markers = cv.connectedComponents(sure_fg)
    logs.append(f"✔ Компоненты: {ret}")

    markers = markers + 1
    markers[unknown == 255] = 0

    markers = cv.watershed(img, markers)
    img[markers == -1] = [255, 0, 0]
    logs.append("✔ Watershed применён")

    return {
        "final": encode_image(img),
        "thresh": encode_image(thresh),
        "opening": encode_image(opening),
        "sure_bg": encode_image(sure_bg),
        "sure_fg": encode_image(sure_fg),
        "unknown": encode_image(unknown),
        "logs": logs
    }

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        data = process_image()

        html = f"""
        <html lang="ru">
        <head>
            <meta charset="UTF-8">
            <title>Watershed Demo</title>
            <style>
                body {{ font-family: Arial; }}
                img {{ max-width: 300px; margin: 10px; }}
                .log {{ background: black; color: lime; padding: 10px; }}
            </style>
        </head>
        <body>

        <h1>Watershed сегментация</h1>

        <h2>Логи:</h2>
        <div class="log">
        {"<br>".join(data["logs"])}
        </div>

        <h2>Результаты:</h2>

        <h3>Итог</h3>
        <img src="data:image/png;base64,{data['final']}"/>

        <h3>Threshold</h3>
        <img src="data:image/png;base64,{data['thresh']}"/>

        <h3>Opening</h3>
        <img src="data:image/png;base64,{data['opening']}"/>

        <h3>Sure BG</h3>
        <img src="data:image/png;base64,{data['sure_bg']}"/>

        <h3>Sure FG</h3>
        <img src="data:image/png;base64,{data['sure_fg']}"/>

        <h3>Unknown</h3>
        <img src="data:image/png;base64,{data['unknown']}"/>

        </body>
        </html>
        """

        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))

def open_browser():
    time.sleep(1)
    webbrowser.open(f"http://localhost:{PORT}")

if __name__ == "__main__":
    server = HTTPServer(("localhost", PORT), Handler)

    print(f"🚀 Запуск: http://localhost:{PORT}")

    threading.Thread(target=open_browser).start()

    server.serve_forever()