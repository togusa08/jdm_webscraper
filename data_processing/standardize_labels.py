import os
import shutil

STANDARD_LABELS = {
    "トヨタ": "Toyota",
    "プリウス": "Prius",
    "ホンダ": "Honda",
    "フィット": "Fit",
    "日産": "Nissan",
    "ノート": "Note",
    "マツダ": "Mazda",
    "スバル": "Subaru",
    "corolla": "Toyota_Corolla",
    "unknown_model": "Unknown_Model"
}

def standardize_directory_names(base_dir="dataset"):
    """
    Scans the dataset directory and renames folders and files natively using os and shutil 
    to match the standardized labels dictionary.
    """
    dataset_path = os.path.abspath(base_dir)
    
    if not os.path.exists(dataset_path):
        print(f"[!] Dataset directory '{base_dir}' not found. Please scrape data first.")
        return

    print(f"[*] Starting standardized label mapping in directory: {dataset_path}")
    
    renamed_count = 0
    
    # Iterate through folders 
    for folder_name in os.listdir(dataset_path):
        old_path = os.path.join(dataset_path, folder_name)
        
        if not os.path.isdir(old_path):
            continue
            
        
        new_name = folder_name
        
        if new_name in STANDARD_LABELS:
            new_name = STANDARD_LABELS[new_name]
        else:
            
            parts = new_name.split('_')
            new_parts = [STANDARD_LABELS.get(part, part) for part in parts]
            new_name = "_".join(new_parts)
            
        if new_name != folder_name:
            new_path = os.path.join(dataset_path, new_name)
            
            if os.path.exists(new_path):
                print(f"[-] Cannot rename '{folder_name}' to '{new_name}' because '{new_name}' already exists. Merging contents...")
                # Merge logic inside here using shutil.move
                for file in os.listdir(old_path):
                    shutil.move(os.path.join(old_path, file), os.path.join(new_path, file))
                os.rmdir(old_path)
            else:
                print(f"[+] Renamed Directory: '{folder_name}' -> '{new_name}'")
                shutil.move(old_path, new_path)
            
            renamed_count += 1

    print(f"\n[*] Standardization complete! Renamed or merged {renamed_count} directories.")

if __name__ == "__main__":
    standardize_directory_names()
