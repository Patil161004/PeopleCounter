"""
Production entry point for Render deployment
"""
import os
from app import app

# Production configuration
app.config.update(
    DEBUG=False,
    UPLOAD_FOLDER='/tmp/uploads',
    PROCESSED_FOLDER='/tmp/processed',
    RESULTS_FOLDER='/tmp/results',
    MAX_CONTENT_LENGTH=50 * 1024 * 1024  # 50MB limit
)

# Ensure temp directories exist
for folder in ['/tmp/uploads', '/tmp/processed', '/tmp/results']:
    os.makedirs(folder, exist_ok=True)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
