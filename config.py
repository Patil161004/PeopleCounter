# Configuration file for People Counter App

# YOLO Model Configuration
# Options: 'yolov8n.pt' (fastest), 'yolov8s.pt' (balanced), 'yolov8m.pt' (most accurate)
YOLO_MODEL = 'yolov8s.pt'  # Using small model for balanced speed/accuracy

# Detection confidence threshold (0.0 to 1.0)
CONFIDENCE_THRESHOLD = 0.3  # Optimized threshold

# Model priority: 'inception' (your trained model), 'ensemble', 'yolo', 'efficientdet'
PRIMARY_MODEL = 'inception'  # Prioritize your custom trained model

# Maximum file size in MB
MAX_FILE_SIZE = 16

# Allowed image extensions
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff']

# Flask configuration
DEBUG_MODE = True
HOST = '0.0.0.0'
PORT = 5000

# Directory names
UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'
RESULTS_FOLDER = 'results'
