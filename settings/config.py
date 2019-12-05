import os

from dotenv import load_dotenv

from settings.paths import BASE_DIR

load_dotenv(
    os.path.join(BASE_DIR, 'settings', 'env')
)
