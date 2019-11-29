from PIL import Image
import tensorflow as tf


def make_square(img, min_size=224, fill_color=(255, 255, 255, 0)) -> Image:
    """
    Делает картинку квадратной с сохранением пропорций
    """
    output_size = min_size, min_size
    x, y = img.size
    max_size = max(x, y)
    coeff = min_size / max_size
    x, y = round(x * coeff), round(y * coeff)
    img = img.resize((x, y), 1)
    size = max(min_size, x, y)
    new_im = Image.new('RGB', (size, size), fill_color)
    new_im.paste(img, (int((size - x) / 2), int((size - y) / 2)))
    new_im.thumbnail(output_size, Image.ANTIALIAS)
    return new_im


def image_to_vector(image_path):
    return tf.keras.preprocessing.image.img_to_array(img=make_square(Image.open(image_path)))

