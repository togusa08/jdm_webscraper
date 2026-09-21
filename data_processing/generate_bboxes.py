import os
from ultralytics import YOLO
import json

# 2: car, 3: motorcycle, 5: bus, 7: truck
TARGET_CLASSES = [2, 5, 7] 

def generate_bounding_boxes(base_dir="dataset"):
    """
    Scans the dataset directory, runs YOLOv8 image inference, 
    and saves bounding box coordinates inside dedicated JSON files.
    """
    dataset_path = os.path.abspath(base_dir)
    
    if not os.path.exists(dataset_path):
        print(f"[!] Dataset directory '{base_dir}' not found. Please scrape data first.")
        return

    print(f"[*] Starting Object Localization (Bounding Boxes) using YOLOv8 in: {dataset_path}")
    print("[*] Automatically downloading/loading ultralytics YOLOv8n (Nano) model...")
    
    try:
        # Load the pre-trained YOLOv8 Nano model 
        model = YOLO("yolov8n.pt") 
    except Exception as e:
        print(f"[!] Failed to load Ultralytics YOLOv8: {e}")
        return
    
    total_boxes = 0

    # Locate all potential images
    image_files = []
    for root, dirs, files in os.walk(dataset_path):
        image_files.extend([os.path.join(root, f) for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png'))])

    for file_path in image_files:
        try:
            results = model.predict(source=file_path, classes=TARGET_CLASSES, verbose=False)
            
            predictions = []
            
            for result in results:
                # Iterate through all detected Bounding Boxes
                for box in result.boxes:
                    # Explicitly exact [x_min, y_min, x_max, y_max] format from the PyTorch tensors
                    xmin, ymin, xmax, ymax = box.xyxy[0].tolist() 
                    conf = box.conf[0].item()
                    cls = int(box.cls[0].item())
                    
                    predictions.append({
                        "class_id": cls,
                        "class_name": result.names[cls],
                        "confidence": round(conf, 4),
                        "bbox_xyxy": [round(xmin, 2), round(ymin, 2), round(xmax, 2), round(ymax, 2)]
                    })
                    total_boxes += 1
            
            if predictions:
                base_name, _ = os.path.splitext(file_path)
                json_path = f"{base_name}_bbox.json"
                with open(json_path, 'w', encoding='utf-8') as f:
                    json.dump(predictions, f, indent=4)
                    
        except Exception as e:
            print(f"[-] Failed to process bounding box for {file_path}: {e}")

    print(f"\n[*] Object Localization Pipeline complete! Extracted {total_boxes} distinct vehicle bounding boxes natively.")

if __name__ == "__main__":
    generate_bounding_boxes()