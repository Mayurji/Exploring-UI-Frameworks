from ultralytics import YOLO
import cv2

# Load the model (using the 'nano' version for speed)
# YOLO11 is the state-of-the-art as of late 2024/2025
model = YOLO("yolo11n.pt") 

def predict_frame(img, conf_threshold, iou_threshold):
    """
    Takes a single frame, runs detection, and returns the annotated frame.
    """
    if img is None:
        return None
    
    # Run inference
    # stream=True ensures efficient memory usage for continuous feeds
    results = model.predict(
        source=img, 
        conf=conf_threshold, 
        iou=iou_threshold, 
        show_labels=True, 
        show_conf=True, 
        imgsz=640
    )
    
    # Plot results on the frame (returns BGR by default, 
    # but Gradio handles numpy arrays well)
    annotated_frame = results[0].plot()
    
    # Convert BGR (OpenCV) to RGB (Gradio/PIL)
    return cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)