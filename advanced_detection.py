"""
Advanced People Counter using TensorFlow Hub EfficientDet
Based on your notebook's approach but with better error handling
"""
import cv2
import numpy as np
import os

# Try to import TensorFlow components
try:
    import tensorflow as tf
    import tensorflow_hub as hub
    TF_AVAILABLE = True
except ImportError:
    TF_AVAILABLE = False
    print("TensorFlow not available")

class EfficientDetCounter:
    def __init__(self):
        self.model = None
        self.load_model()
    
    def load_model(self):
        """Load EfficientDet model from TensorFlow Hub"""
        if not TF_AVAILABLE:
            print("❌ TensorFlow not available for EfficientDet")
            return
        
        try:
            print("Loading EfficientDet D1 model from TensorFlow Hub...")
            # Using D1 model which is more accurate than D0 for crowded scenes
            self.model = hub.load('https://tfhub.dev/tensorflow/efficientdet/d1/1')
            print("✅ EfficientDet D1 model loaded successfully")
        except Exception as e:
            print(f"❌ Error loading EfficientDet D1, falling back to D0: {e}")
            try:
                self.model = hub.load('https://tfhub.dev/tensorflow/efficientdet/d0/1')
                print("✅ EfficientDet D0 model loaded successfully")
            except Exception as e2:
                print(f"❌ Error loading EfficientDet D0: {e2}")
                self.model = None
    
    def detect_objects(self, image_path):
        """Detect objects in image using EfficientDet with enhanced preprocessing"""
        if self.model is None:
            return None
        
        try:
            # Load and preprocess image exactly as in your notebook
            image_string = tf.io.read_file(image_path)
            image_tensor = tf.image.decode_jpeg(image_string, channels=3)
            
            # Ensure image is in proper format and size
            image_tensor = tf.cast(image_tensor, tf.uint8)
            
            # Add batch dimension
            image_tensor = image_tensor[tf.newaxis, ...]
            
            print(f"Processing image with shape: {image_tensor.shape}")
            return self.model(image_tensor)
        except Exception as e:
            print(f"Error in object detection: {e}")
            return None
    
    def count_persons(self, image_path, threshold=0.25):
        """Count people using EfficientDet with the logic from your notebook"""
        try:
            results = self.detect_objects(image_path)
            if results is None:
                return 0
            
            # Extract detection results
            classes = results['detection_classes'].numpy()[0]
            scores = results['detection_scores'].numpy()[0]
            
            # Count persons (class ID 1 = "person" in COCO dataset)
            person_count = (classes == 1)[np.where(scores > threshold)].sum()
            return int(person_count)
            
        except Exception as e:
            print(f"Error counting persons: {e}")
            return 0
    
    def draw_bboxes(self, image_path, threshold=0.25):
        """Draw bounding boxes like in your notebook"""
        try:
            results = self.detect_objects(image_path)
            if results is None:
                return None
            
            # Load original image
            image = cv2.imread(image_path)
            if image is None:
                return None
            
            # Convert to RGB for PIL compatibility
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Get image dimensions
            im_height, im_width = image.shape[:2]
            
            # Extract detection data
            boxes = results['detection_boxes'].numpy()[0]
            classes = results['detection_classes'].numpy()[0]
            scores = results['detection_scores'].numpy()[0]
            num_detections = int(results['num_detections'][0])
            
            person_count = 0
            
            # Draw bounding boxes for detected persons
            for i in range(num_detections):
                if classes[i] == 1 and scores[i] > threshold:  # Person class
                    person_count += 1
                    
                    # Get box coordinates (normalized)
                    ymin, xmin, ymax, xmax = boxes[i]
                    
                    # Convert to pixel coordinates
                    left = int(xmin * im_width)
                    right = int(xmax * im_width)
                    top = int(ymin * im_height)
                    bottom = int(ymax * im_height)
                    
                    # Draw rectangle
                    cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 3)
                    
                    # Add label
                    label = f'Person {person_count} ({scores[i]:.2f})'
                    cv2.putText(image, label, (left, top-10), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            # Add summary
            summary = f'EfficientDet: {person_count} people detected'
            cv2.rectangle(image, (10, 10), (500, 50), (0, 0, 0), -1)
            cv2.putText(image, summary, (15, 35), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
            
            return image, person_count
            
        except Exception as e:
            print(f"Error drawing bboxes: {e}")
            return None, 0

# Global detector instance
efficient_det = None

def initialize_efficientdet():
    """Initialize EfficientDet detector"""
    global efficient_det
    if efficient_det is None:
        efficient_det = EfficientDetCounter()
    return efficient_det.model is not None

def count_people_efficientdet_method(image_path):
    """
    Count people using EfficientDet (from your notebook approach)
    """
    try:
        global efficient_det
        
        if efficient_det is None:
            efficient_det = EfficientDetCounter()
        
        if efficient_det.model is None:
            print("EfficientDet model not available")
            return 0, None, "EfficientDet Unavailable"
        
        print(f"Using EfficientDet for {os.path.basename(image_path)}")
        
        # Count with different thresholds - including lower ones for crowded scenes
        # Using exact values to avoid floating point precision issues
        thresholds = [0.1, 0.15, 0.2, 0.25, 0.3, 0.5]  # Temporarily remove 0.23 to test
        results = {}
        
        print(f"  Testing thresholds: {thresholds}")
        
        for thresh in thresholds:
            try:
                count = efficient_det.count_persons(image_path, thresh)
                results[thresh] = count
                print(f"  Threshold {thresh}: {count} people")
            except Exception as e:
                print(f"  Error testing threshold {thresh}: {e}")
                results[thresh] = 0
        
        # Manually test 0.23 with better error handling
        try:
            count_23 = efficient_det.count_persons(image_path, 0.23)
            results[0.23] = count_23
            print(f"  Threshold 0.23: {count_23} people")
        except Exception as e:
            print(f"  Error testing threshold 0.23: {e}")
            results[0.23] = 0
        
        print(f"  Results dictionary: {results}")
        
        # Smart threshold selection: prefer 0.23 threshold for better detection
        final_threshold = 0.23
        final_count = results.get(0.23, 0)
        
        print(f"  Attempting to use threshold {final_threshold}, count: {final_count}")
        
        # If very few detections at 0.23, try lower thresholds
        if final_count < 5:
            if 0.15 in results and results[0.15] > final_count:
                final_threshold = 0.15
                final_count = results[final_threshold]
                print(f"  Using lower threshold {final_threshold} for better detection")
            elif 0.1 in results and results[0.1] > final_count:
                final_threshold = 0.1
                final_count = results[final_threshold]
                print(f"  Using lowest threshold {final_threshold} for better detection")
        
        # Create annotated image
        annotated_image, _ = efficient_det.draw_bboxes(image_path, final_threshold)
        
        print(f"  Final result: {final_count} people (threshold: {final_threshold})")
        
        return final_count, annotated_image, f"EfficientDet (threshold: {final_threshold})"
        
    except Exception as e:
        print(f"Error in EfficientDet method: {e}")
        return 0, None, "EfficientDet Error"

def count_people_smart_hybrid(image_path):
    """
    Smart hybrid approach prioritizing EfficientDet (your notebook method)
    """
    try:
        print(f"Smart hybrid detection for {os.path.basename(image_path)}")
        
        # Use EfficientDet (from your notebook)
        efficientdet_count, efficientdet_image, efficientdet_method = count_people_efficientdet_method(image_path)
        
        return efficientdet_count, efficientdet_image, efficientdet_method
                
    except Exception as e:
        print(f"Error in smart hybrid: {e}")
        return 0, None, "Error"
