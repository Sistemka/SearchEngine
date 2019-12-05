import numpy as np
from keras.applications import VGG19
from keras.applications.vgg19 import preprocess_input
from keras.engine import Model
from keras.preprocessing import image
from sklearn.neighbors import NearestNeighbors

from utils import load_sparse_matrix, image_manager
from settings.paths import VECTORS_PATH


def _vectorize(path, model):
    img = image.load_img(path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    pred = model.predict(x)
    return pred.ravel()


def _similar(vec, knn, urls, n_neighbors=6):
    dist, indices = knn.kneighbors(vec.reshape(1, -1), n_neighbors=n_neighbors)
    dist, indices = dist.flatten(), indices.flatten()
    return [(urls[indices[i]], dist[i]) for i in range(len(indices))]


def load_predictor():
    urls = image_manager.get_urls()
    vecs = load_sparse_matrix(VECTORS_PATH)
    base_model = VGG19(weights='imagenet')
    model = Model(inputs=base_model.input, outputs=base_model.get_layer('fc1').output)
    knn = NearestNeighbors(metric='cosine', algorithm='brute')
    knn.fit(vecs)

    def similarity(file_path, n_neighbors=6):
        vec = _vectorize(file_path, model)
        return _similar(vec, knn, urls, n_neighbors)

    return similarity


predictor = load_predictor()
