from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
FILES_DIR = Path(BASE_DIR, 'files')
MODELS_DIR = Path(BASE_DIR, 'models')
MODEL_PATH = Path(MODELS_DIR, 'model.h5')
