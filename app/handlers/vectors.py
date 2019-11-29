import os
from pathlib import Path

from flask import jsonify
from flask_restplus import Resource, Namespace
from werkzeug.utils import secure_filename

from src import image_to_vector
from app.app import basic_args, image_args
from models import Vectors
from settings.paths import BASE_DIR


ns = Namespace(
    'vectors',
    description='VectorManager',
    validate=True
)


@ns.route('/add')
@ns.expect(basic_args)
class AddVector(Resource):
    @ns.expect(image_args)
    def post(self):
        basic_args.parse_args()

        args = image_args.parse_args()
        image = args['image']
        image_name = secure_filename(image.filename)
        image_path_tmp = args['url'].split('/')[: -1]
        image_path = Path(BASE_DIR, *image_path_tmp, image_name).as_posix()
        image.save(image_path)

        res = image_to_vector(image_path=image_path)
        v = Vectors.create(
            type=args['type'],
            url=args['url'],
            vector=res.tostring()
        )
        os.remove(image_path)

        return jsonify({
            'error': False,
            'message': f'added {v.id}'
        })


def register(main_api):
    main_api.add_namespace(ns)
