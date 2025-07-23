# Configuration file for People Counter App
import os

# Environment detection
IS_PRODUCTION = os.environ.get('RENDER') or os.environ.get('PORT')

# EfficientDet Configuration
CONFIDENCE_THRESHOLD = 0.23  # Optimized threshold for people detection
EFFICIENTDET_MODEL_URL = 'https://tfhub.dev/tensorflow/efficientdet/d1/1'

# File upload settings
MAX_FILE_SIZE = 50 if IS_PRODUCTION else 16  # MB
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff']

# Directory configuration
if IS_PRODUCTION:
    # Production paths (Render uses /tmp for temporary files)
    UPLOAD_FOLDER = '/tmp/uploads'
    PROCESSED_FOLDER = '/tmp/processed'
    RESULTS_FOLDER = '/tmp/results'
    DEBUG_MODE = False
else:
    # Local development paths
    UPLOAD_FOLDER = 'uploads'
    PROCESSED_FOLDER = 'processed'
    RESULTS_FOLDER = 'results'
    DEBUG_MODE = True

# Flask configuration
PORT = int(os.environ.get('PORT', 5000))
HOST = '0.0.0.0'
PORT = 5000

# Directory names
UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'
RESULTS_FOLDER = 'results' 