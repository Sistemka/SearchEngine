import os
from pathlib import Path

import numpy as np
import scipy.sparse as sp
from keras.engine import Model
from keras.applications import VGG19
from keras.applications.vgg19 import preprocess_input
from keras.preprocessing import image

from utils import image_manager, save_sparse_matrix
from settings.paths import TMP_IMAGES_DIR, VECTORS_PATH


def create_vectors(urls, model, px=224, n_dims=512, batch_size=512):
    min_idx = 0
    max_idx = min_idx + batch_size
    total_max = len(urls)
    preds = sp.lil_matrix((len(urls), n_dims))

    while min_idx < total_max - 1:
        X = np.zeros(((max_idx - min_idx), px, px, 3))
        i = 0
        for i in range(min_idx, max_idx):
            url = urls[i]
            file_path = Path(TMP_IMAGES_DIR, url).as_posix()
            image_manager.download_image(
                url=url,
                path_to_download=file_path
            )
            try:
                img = image.load_img(file_path, target_size=(px, px))
                img_array = image.img_to_array(img)
                X[i - min_idx, :, :, :] = img_array
            except Exception:
                pass
            os.remove(file_path)
        max_idx = i
        X = preprocess_input(X)
        these_preds = model.predict(X)
        shp = ((max_idx - min_idx) + 1, n_dims)
        preds[min_idx:max_idx + 1, :] = these_preds.reshape(shp)
        min_idx = max_idx
        max_idx = np.min((max_idx + batch_size, total_max))
    return preds


def indexing():
    base_model = VGG19(weights='imagenet')
    urls = image_manager.get_urls()
    model = Model(inputs=base_model.input, outputs=base_model.get_layer('fc1').output)
    vectors = create_vectors(urls=urls, model=model, n_dims=4096)
    save_sparse_matrix(VECTORS_PATH, vectors)
