from flask import Flask, render_template, request, send_file, flash, redirect, url_for
import os
import cv2
import pandas as pd
from datetime import datetime
import zipfile
import numpy as np
from werkzeug.utils import secure_filename
import config
from advanced_detection import count_people_smart_hybrid, initialize_efficientdet

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Configuration
UPLOAD_FOLDER = config.UPLOAD_FOLDER
PROCESSED_FOLDER = config.PROCESSED_FOLDER
RESULTS_FOLDER = config.RESULTS_FOLDER
ALLOWED_EXTENSIONS = set(config.ALLOWED_EXTENSIONS)

# Create directories
for folder in [UPLOAD_FOLDER, PROCESSED_FOLDER, RESULTS_FOLDER]:
    if not os.path.exists(folder):
        os.makedirs(folder)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def count_people_in_image(image_path):
    """
    Main function using the smart hybrid approach
    Prioritizes EfficientDet (from your notebook) with OpenCV fallback
    """
    try:
        filename = os.path.basename(image_path)
        print(f"Processing {filename}...")
        
        # Use smart hybrid method (EfficientDet first, then OpenCV)
        count, annotated_image, method_used = count_people_smart_hybrid(image_path)
        
        if annotated_image is not None:
            # Add timestamp and method info
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cv2.putText(annotated_image, f"Processed: {timestamp}", (15, annotated_image.shape[0] - 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            cv2.putText(annotated_image, f"Method: {method_used}", (15, annotated_image.shape[0] - 10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            # Save processed image
            processed_path = os.path.join(PROCESSED_FOLDER, f"processed_{filename}")
            cv2.imwrite(processed_path, annotated_image)
        else:
            processed_path = None
        
        print(f"✅ Final result: {count} people in {filename} using {method_used}")
        return count, processed_path
        
    except Exception as e:
        print(f"❌ Error processing {image_path}: {e}")
        return 0, None

def process_images(image_paths):
    """Process multiple images"""
    results = []
    
    print(f"Processing {len(image_paths)} images...")
    
    for i, image_path in enumerate(image_paths, 1):
        filename = os.path.basename(image_path)
        print(f"\n[{i}/{len(image_paths)}] Processing {filename}")
        
        count, processed_path = count_people_in_image(image_path)
        
        results.append({
            'image_name': filename,
            'people_count': count,
            'processed_image_path': processed_path,
            'original_image_path': image_path
        })
    
    return results

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    if 'files' not in request.files:
        flash('No files selected')
        return redirect(request.url)
    
    files = request.files.getlist('files')
    
    if not files or files[0].filename == '':
        flash('No files selected')
        return redirect(url_for('index'))
    
    # Save uploaded files
    uploaded_files = []
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{timestamp}_{filename}"
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
            uploaded_files.append(filepath)
    
    if not uploaded_files:
        flash('No valid image files uploaded')
        return redirect(url_for('index'))
    
    # Process images
    try:
        results = process_images(uploaded_files)
        
        # Create Excel file
        df = pd.DataFrame(results)[['image_name', 'people_count']]
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        excel_filename = f"people_count_results_{timestamp}.xlsx"
        excel_path = os.path.join(RESULTS_FOLDER, excel_filename)
        
        df.to_excel(excel_path, index=False)
        
        # Create zip file with processed images
        zip_filename = f"processed_images_{timestamp}.zip"
        zip_path = os.path.join(RESULTS_FOLDER, zip_filename)
        
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for result in results:
                if result['processed_image_path'] and os.path.exists(result['processed_image_path']):
                    zipf.write(result['processed_image_path'], 
                             f"processed_{result['image_name']}")
        
        return render_template('results.html', 
                             results=results, 
                             excel_file=excel_filename,
                             zip_file=zip_filename,
                             total_images=len(results),
                             total_people=sum(r['people_count'] for r in results))
    
    except Exception as e:
        flash(f'Error processing images: {str(e)}')
        return redirect(url_for('index'))

@app.route('/download/<filename>')
def download_file(filename):
    try:
        file_path = os.path.join(RESULTS_FOLDER, filename)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        else:
            flash('File not found')
            return redirect(url_for('index'))
    except Exception as e:
        flash(f'Error downloading file: {str(e)}')
        return redirect(url_for('index'))

@app.route('/clear')
def clear_files():
    """Clear all files"""
    try:
        for folder in [UPLOAD_FOLDER, PROCESSED_FOLDER, RESULTS_FOLDER]:
            for filename in os.listdir(folder):
                file_path = os.path.join(folder, filename)
                if os.path.isfile(file_path):
                    os.unlink(file_path)
        flash('All files cleared successfully')
    except Exception as e:
        flash(f'Error clearing files: {str(e)}')
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    print("🚀 Starting Advanced People Counter Application")
    print("Based on your notebook's approach with EfficientDet + OpenCV fallback")
    print("")
    
    # Initialize EfficientDet
    print("Initializing AI models...")
    efficientdet_ready = initialize_efficientdet()
    
    if efficientdet_ready:
        print("✅ EfficientDet model ready (Primary method - from your notebook)")
    else:
        print("⚠️  EfficientDet not available, will use OpenCV methods")
    
    print("✅ OpenCV methods ready (Fallback)")
    print("")
    print("🌐 Starting Flask application...")
    app.run(debug=True, host='0.0.0.0', port=5000)
