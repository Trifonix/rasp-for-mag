from PIL import Image, ImageFilter

images = ["7-1_foto.jpg", "7-2_foto.jpg"]

filters = [
    ImageFilter.BLUR,
    ImageFilter.CONTOUR,
    ImageFilter.DETAIL,
    ImageFilter.EDGE_ENHANCE,
    ImageFilter.EDGE_ENHANCE_MORE,
    ImageFilter.EMBOSS,
    ImageFilter.FIND_EDGES,
    ImageFilter.SHARPEN,
    ImageFilter.SMOOTH,
    ImageFilter.SMOOTH_MORE,
]

for path in images:
    try:
        im = Image.open(path)

        # показать оригинал
        im.show()

        # применить фильтры
        for f in filters:
            im_filtered = im.filter(f)
            im_filtered.show()

        # задание 2: контуры
        edges = im.filter(ImageFilter.FIND_EDGES)
        edges.show()

    except Exception as e:
        print(f"Ошибка с файлом {path}: {e}")
