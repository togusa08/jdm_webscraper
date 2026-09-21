import os
import cv2
import torch
import imagehash
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
import glob
import warnings

# Suppress HuggingFace warnings for cleaner output
warnings.filterwarnings("ignore")

# Constants
DATASET_DIR = "dataset"
BLUR_THRESHOLD = 100.0  # OpenCV Laplacian variance threshold
HASH_DIFFERENCE_THRESHOLD = 5  # Hamming distance for duplicates

CLASSES = [
    "a photo of the exterior of a car", 
    "a photo of a car interior", 
    "a photo of a steering wheel", 
    "a logo or text"
]
EXTERIOR_CLASS_INDEX = 0  # "a photo of the exterior of a car" is at index 0

def check_corruption(file_path):
    """Returns True if corrupted, False if OK."""
    try:
        with Image.open(file_path) as img:
            img.verify()
        return False
    except Exception as e:
        print(f"[-] Corrupted image [{file_path}]: {e}")
        return True

def check_blur(file_path, threshold=BLUR_THRESHOLD):
    """Returns True if blurry, False if OK."""
    try:
        # Load grayscale
        image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
        if image is None:
            return True # Failed to load
        variance = cv2.Laplacian(image, cv2.CV_64F).var()
        if variance < threshold:
            print(f"[-] Blurry image [{file_path}] (variance: {variance:.2f} < {threshold})")
            return True
        return False
    except Exception as e:
        print(f"[-] Error checking blur [{file_path}]: {e}")
        return True

def check_duplicates(directory):
    """Uses pHash to find and remove duplicates inside a directory."""
    hashes = {}
    
    # Get all .jpg, .png files
    files = glob.glob(os.path.join(directory, "*.[jJ][pP][gG]")) + glob.glob(os.path.join(directory, "*.[pP][nN][gG]"))
    
    for file_path in files:
        if not os.path.exists(file_path):
            continue
            
        try:
            with Image.open(file_path) as img:
                # Convert to RGB to ensure consistent hashing
                h = imagehash.phash(img.convert('RGB'))
            
            # Check against existing hashes
            duplicate_found = False
            for existing_hash, existing_file in hashes.items():
                if h - existing_hash < HASH_DIFFERENCE_THRESHOLD:
                    print(f"[-] Duplicate found: {file_path} is a duplicate of {os.path.basename(existing_file)} (Hamming dist < {HASH_DIFFERENCE_THRESHOLD})")
                    os.remove(file_path)
                    duplicate_found = True
                    break
                    
            if not duplicate_found:
                hashes[h] = file_path
                
        except Exception as e:
            print(f"[-] Error hashing {file_path}: {e}")

class ImageClassifier:
    def __init__(self):
        print("[*] Loading CLIP model (openai/clip-vit-base-patch32)...")
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(self.device)
        self.processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
        print(f"[*] Model loaded on {self.device.upper()}")

    def is_garbage(self, file_path):
        """Returns True if the image is NOT an exterior car shot."""
        try:
            with Image.open(file_path) as img:
                image = img.convert('RGB')
                inputs = self.processor(text=CLASSES, images=image, return_tensors="pt", padding=True).to(self.device)
                
                with torch.no_grad():
                    outputs = self.model(**inputs)
                
                # Image-text similarity score
                logits_per_image = outputs.logits_per_image
                probs = logits_per_image.softmax(dim=1)
                
                # Get the predicted class index
                predicted_class_idx = probs.argmax().item()
                
                if predicted_class_idx != EXTERIOR_CLASS_INDEX:
                    print(f"[-] Garbage image removed [{file_path}] classified as: '{CLASSES[predicted_class_idx]}' (prob: {probs[0][predicted_class_idx]:.2f})")
                    return True
                return False
        except Exception as e:
            print(f"[-] Error classifying {file_path}: {e}")
            return True

def process_directory():
    dataset_path = os.path.abspath(DATASET_DIR)
    if not os.path.exists(dataset_path):
        print(f"[!] Dataset directory '{DATASET_DIR}' not found. Please scrape some data first.")
        return

    print(f"[*] Starting Image Processing on dataset: {dataset_path}")
    
    # Phase 1: Fast filtering (Corruption, Blur)
    print("\n--- Phase 1: Fast Filtering (Corruption & Blur) ---")
    for root, dirs, files in os.walk(dataset_path):
        for file in files:
            if not file.lower().endswith(('.jpg', '.jpeg', '.png')):
                continue
            file_path = os.path.join(root, file)
            
            # Check Corruption
            if check_corruption(file_path):
                if os.path.exists(file_path): os.remove(file_path)
                continue
                
            # Check Blur
            if check_blur(file_path):
                if os.path.exists(file_path): os.remove(file_path)
                continue

    # Phase 2: Duplicate detection (Per Directory)
    print("\n--- Phase 2: Duplicate Detection (Per Model) ---")
    for root, dirs, files in os.walk(dataset_path):
        if root != dataset_path: # Skip the base 'dataset' folder itself
            check_duplicates(root)

    # Phase 3: Semantic classification (Slow)
    print("\n--- Phase 3: Semantic Classification (CLIP) ---")
    # First check if there are any images left
    has_images = any(file.lower().endswith(('.jpg', '.png')) 
                    for _, _, files in os.walk(dataset_path) 
                    for file in files)
                    
    if has_images:
        classifier = ImageClassifier()
        for root, dirs, files in os.walk(dataset_path):
            for file in files:
                if not file.lower().endswith(('.jpg', '.jpeg', '.png')):
                    continue
                file_path = os.path.join(root, file)
                
                if classifier.is_garbage(file_path):
                    if os.path.exists(file_path): os.remove(file_path)
    else:
        print("[*] No images remaining to classify.")
                
    print("\n[*] Image cleaning complete!")

if __name__ == "__main__":
    process_directory()
