from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


FILES_DIR = Path(BASE_DIR, 'files')
FILES_DIR.mkdir(parents=True, exist_ok=True)

TMP_IMAGES_DIR = Path(BASE_DIR, 'images')
TMP_IMAGES_DIR.mkdir(parents=True, exist_ok=True)

VECTORS_PATH = Path(BASE_DIR, 'vectors', 'vectors.npz')
VECTORS_PATH.parent.mkdir(parents=True, exist_ok=True)
