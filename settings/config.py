import os

from dotenv import load_dotenv

from settings.paths import BASE_DIR

load_dotenv(
    os.path.join(BASE_DIR, 'settings', 'env')
)

PG_CONN = {
    'host': os.environ.get('PG_HOST', 'localhost'),
    'database': os.environ.get('PG_DATABASE'),
    'user': os.environ.get('PG_USER'),
    'password': os.environ.get('PG_PASSWORD'),
    'autorollback': True,
}
