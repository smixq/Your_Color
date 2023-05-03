from PIL import Image
import io
import base64


def resize_img(img):
    img = Image.open(io.BytesIO(img))
    w, h = img.size
    if w != h:
        delta = abs(h - w) // 2
        if w > h:
            img = img.crop((delta, 0, w - delta, h))
        else:
            img = img.crop((0, delta, w, h - delta))
    # io_bytes = io.BytesIO()
    # img.save(io_bytes, format=img.format)
    # im_bytes = base64.b64encode(img)
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    byte_im = buf.getvalue()
    return byte_im
