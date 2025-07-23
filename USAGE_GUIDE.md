# 🚀 People Counter Web Application - Quick Start Guide

## 🎯 What This Application Does

This Flask web application uses **EfficientDet AI model** to automatically count people in uploaded images and provides results in Excel format with download options.

### ✨ Key Features
- **Multiple Image Upload** - Upload multiple images at once
- **AI-Powered Detection** - Uses state-of-the-art EfficientDet for accurate people counting
- **Visual Results** - See processed images with bounding boxes around detected people
- **Excel Export** - Download results in Excel format with image names and counts
- **Batch Processing** - Process multiple images simultaneously
- **Modern UI** - Responsive drag-and-drop interface

## 🏃‍♂️ Quick Start

### Option 1: Use the Startup Script (Recommended)
1. **Double-click `start.bat`** - This will automatically:
   - Create a virtual environment
   - Install all dependencies
   - Start the application

### Option 2: Manual Setup
1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application**:
   ```bash
   python app.py
   ```

3. **Open your browser** and go to: http://localhost:5000

## 📱 How to Use

### Step 1: Upload Images
- Drag and drop images onto the upload area, OR
- Click "Choose Images" to select files
- Supported formats: PNG, JPG, JPEG, GIF, BMP, TIFF

### Step 2: Process Images
- Click "Process Images"
- Wait for AI analysis to complete
- View the results summary

### Step 3: Download Results
- **Excel Report**: Download spreadsheet with image names and people counts
- **Processed Images**: Download ZIP file with annotated images showing detected people

## 🎯 Testing the Application

Demo images are included for testing:
- `sample_people_image.jpg` - Real photo with people
- `demo_people_image.jpg` - Synthetic image with 5 person-like shapes
- `test_image.jpg` - Basic test image

## 📊 Understanding Results

### Excel Output
| Image Name | People Count |
|------------|-------------|
| photo1.jpg | 3 |
| photo2.jpg | 7 |
| photo3.jpg | 2 |

### Processed Images
- Original images with green bounding boxes around detected people
- Confidence scores displayed for each detection
- All processed images available in downloadable ZIP file

## ⚙️ Configuration

Edit `config.py` to customize:
- **DETECTION_MODEL**: Uses EfficientDet from TensorFlow Hub (automatic download)
- **CONFIDENCE_THRESHOLD**: Adjust detection sensitivity (0.1 to 0.9)
- **PORT**: Change the web server port (default: 5000)

## 🔧 Troubleshooting

### Common Issues

1. **"EfficientDet model failed to load"**
   - The app will use fallback methods with reduced accuracy
   - First run takes longer as the AI model downloads from TensorFlow Hub

2. **Port 5000 already in use**
   - Change PORT in `config.py` to a different number (e.g., 5001)

3. **Out of memory errors**
   - Use smaller images or process fewer images at once
   - The EfficientDet D1 model requires more memory but provides better accuracy

4. **Slow processing**
   - Normal for first run (model download + initialization)
   - EfficientDet provides high accuracy but may be slower than simpler models

### Performance Tips
- **For Speed**: Model will optimize after first few runs
- **For Accuracy**: EfficientDet D1 provides excellent accuracy for crowded scenes
- **Memory**: Reduce image sizes if experiencing memory issues

## 📁 File Structure

```
PeopleCounter/
├── app.py                    # Main Flask application with EfficientDet
├── advanced_detection.py     # EfficientDet implementation
├── config.py                 # Configuration settings
├── requirements.txt          # Python dependencies
├── start.bat                 # Windows startup script
├── templates/               # Web interface
│   ├── index.html          # Upload page
│   └── results.html        # Results page
├── uploads/                 # Uploaded images (auto-created)
├── processed/              # Processed images (auto-created)
└── results/                # Excel files and downloads (auto-created)
```

## 🎨 Customization

### Change Detection Sensitivity
In `config.py`, adjust:
```python
CONFIDENCE_THRESHOLD = 0.15  # Lower = more detections, Higher = more strict
```

### Model Configuration
The application uses EfficientDet D1 from TensorFlow Hub:
- Automatically downloads on first run
- High accuracy for crowded scenes
- Optimized for people detection

### Modify Web Interface
- Edit `templates/index.html` for upload page
- Edit `templates/results.html` for results page
- CSS styles are embedded in the HTML files

## 🔒 Security Notes

- Files are temporarily stored and can be cleared using "Clear All Files"
- Only image files are accepted for upload
- Processed files are automatically cleaned up
- No data is stored permanently unless you download it

## 🚀 Deployment Notes

For production deployment:
1. Change `DEBUG_MODE = False` in `config.py`
2. Use a production WSGI server (e.g., Gunicorn)
3. Set up proper file permissions and storage
4. Consider using cloud storage for large file handling

## 📞 Support

If you encounter any issues:
1. Check the terminal output for error messages
2. Verify all dependencies are installed: `pip list`
3. Test with the provided demo images first
4. Check that Python 3.8+ is installed

## 🎉 Success Checklist

✅ Application starts without errors  
✅ Web interface loads at http://localhost:5000  
✅ Can upload images successfully  
✅ Processing completes with people count results  
✅ Excel file downloads correctly  
✅ Processed images ZIP file downloads correctly  

---

**Ready to count some people? Open http://localhost:5000 and start uploading images! 📸👥**
