from models import Vectors
import numpy as np

from keras.models import load_model
from settings.paths import MODEL_PATH


all_labels = {
        'pants', 'sweaters', 'shorts',
        'type1', 'shirts', 'jackets',
        'scarfs', 'boots', 'caps', 'sneakers'
    }

model = load_model(MODEL_PATH)


def predict(
        input_tensor,
        next_step_accuracy_percent=0.5,
        next_step_point=2,
        comparing_percent=0.8
):
    matching_items = []
    for label in all_labels:
        currently_accepted_items = []
        comparing_list = []
        all_vectors = Vectors.select().where(Vectors.type == label)
        for v in all_vectors:
            vec = np.frombuffer(v.vector, dtype='float32').reshape((224, 224, 3))
            comparing_tensor = np.expand_dims(vec, 0)
            compare_result = model.predict([input_tensor, comparing_tensor])[0][0]
            comparing_list.append(compare_result)
            if compare_result > comparing_percent:
                currently_accepted_items.append({"url": v.url, "type": label})
            if len(comparing_list) > next_step_point and sum(comparing_list) / len(comparing_list) < next_step_accuracy_percent:
                break
        matching_items.extend(currently_accepted_items)
    return matching_items
