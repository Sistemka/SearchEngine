from models import Vectors
import numpy as np

from keras.models import load_model
from settings.paths import MODEL_PATH



labels = {
        'pants', 'sweaters', 'shorts',
        'type1', 'shirts', 'jackets',
        'scarfs', 'boots', 'caps', 'sneakers'
    }

model = load_model(MODEL_PATH)


def predict(new_image):
    counter = 0
    results = []
    for label in labels:
        vectors = Vectors.select().where(Vectors.type == label)
        for v in vectors:
            vec = np.frombuffer(v.vector, dtype='float32').reshape((224, 224, 3))
            result = model.predict([np.expand_dims(vec, 0), new_image])
            if counter >= 5:
                counter = 0
                break
            if result[0][0] < 0.6:
                counter += 1
            else:
                results.append((v.url, result[0][0], v.type))

    return [
        {
            'url': item[0],
            'type': item[2]
        }
        for item in
        sorted(results, reverse=True, key=lambda tup: tup[1])[:3]
    ]
