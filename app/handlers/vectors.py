import os
from pathlib import Path

from flask import jsonify
from flask_restplus import Resource, Namespace

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
        image_path = Path(BASE_DIR, *args['url'].split('/')).as_posix()
        image.save(image_path)

        res = image_to_vector(image_path=image_path)
        os.remove(image_path)
        v = Vectors.create(
            type=args['type'],
            url=args['url'],
            vector=res.tostring()
        )
        return jsonify({
            'error': False,
            'message': f'added {v.id}'
        })


def register(main_api):
    main_api.add_namespace(ns)
