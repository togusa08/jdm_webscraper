import os
import cv2
import albumentations as A

AUGMENTATION_MULTIPLIER = 3

# Define the Albumentations transformation pipeline
# To implement your specified Bounding Box Coordinates multiplication in the future:
# Change this to -> A.Compose([...], bbox_params=A.BboxParams(format='pascal_voc', label_fields=['category_labels']))
aug_pipeline = A.Compose([
    A.HorizontalFlip(p=0.5), 
    A.RandomBrightnessContrast(p=0.5), 
    A.ShiftScaleRotate(shift_limit=0.0625, scale_limit=0.1, rotate_limit=15, p=0.5), 
    A.GaussNoise(p=0.2), 
])

def augment_dataset(base_dir="dataset"):
    """
    Scans the dataset directory, reads images, applies albumentations random transformations,
    and saves new synthetic variations to expand the dataset size.
    """
    dataset_path = os.path.abspath(base_dir)
    
    if not os.path.exists(dataset_path):
        print(f"[!] Dataset directory '{base_dir}' not found. Please scrape data first.")
        return

    print(f"[*] Starting Synthetic Expansion (Data Augmentation) in: {dataset_path}")
    print(f"[*] Generating {AUGMENTATION_MULTIPLIER} augmented variations per original image...")

    total_augmented = 0

    
    for root, dirs, files in os.walk(dataset_path):
        
        # Filter for valid images 
        image_files = [f for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        
        for file in image_files:
            if "_aug_" in file:
                continue

            file_path = os.path.join(root, file)
            
            try:
                image = cv2.imread(file_path)
                if image is None:
                    continue
                    
                image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

                for i in range(AUGMENTATION_MULTIPLIER):
                    transformed = aug_pipeline(image=image_rgb)
                    transformed_image = transformed["image"]
                    
                    
                    transformed_bgr = cv2.cvtColor(transformed_image, cv2.COLOR_RGB2BGR)
                    
                    base_name, ext = os.path.splitext(file)
                    new_file_name = f"{base_name}_aug_{i}{ext}"
                    new_file_path = os.path.join(root, new_file_name)
                    
                  
                    cv2.imwrite(new_file_path, transformed_bgr)
                    total_augmented += 1
            except Exception as e:
                print(f"[-] Failed to augment {file}: {e}")
                
    print(f"\n[*] Data Augmentation complete! Generated {total_augmented} new synthetic images.")

if __name__ == "__main__":
    augment_dataset()
