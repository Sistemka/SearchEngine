import os
from pathlib import Path

import numpy as np
from flask import jsonify
from flask_restplus import Resource, Namespace
from werkzeug.utils import secure_filename

from src import image_to_vector, predict
from app.app import basic_args, predict_image_args
from settings.paths import FILES_DIR

ns = Namespace(
    '',
    description='SearchEngine',
    validate=True
)


@ns.route('/predict')
@ns.expect(basic_args)
class Predict(Resource):
    @ns.expect(predict_image_args)
    def post(self):
        basic_args.parse_args()
        args = predict_image_args.parse_args()
        image = args['image']
        image_name = secure_filename(image.filename)
        image_path = Path(FILES_DIR, image_name).as_posix()
        image.save(image_path)
        new_vector = np.expand_dims(image_to_vector(image_path=image_path), 0)

        prediction = predict(new_vector)

        os.remove(image_path)
        return jsonify({
            'error': False,
            'result': prediction
        })


def register(main_api):
    main_api.add_namespace(ns)
