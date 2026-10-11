import zipfile
import os
from datetime import datetime

def zip_project():
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    zip_filename = f"Lifeline_Pharmacy_Backup_{timestamp}.zip"
    
    # Exclude these logical patterns
    excludes = {
        '__pycache__', 
        '.git', 
        '.vscode', 
        '.gemini', 
        'venv', 
        'env', 
        '.pytest_cache',
        'node_modules'
    }
    
    print(f"Creating backup: {zip_filename}...")
    
    try:
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk('.'):
                # Modify dirs in-place to exclude unwanted directories
                dirs[:] = [d for d in dirs if d not in excludes]
                
                for file in files:
                    if file == zip_filename:
                        continue # Don't include the zip file itself
                    if file.endswith('.pyc') or file.endswith('.pyo'):
                        continue
                        
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, '.')
                    
                    print(f"Adding: {arcname}")
                    zipf.write(file_path, arcname)
                    
        print(f"\n✅ SUCCESS! Project saved as: {os.path.abspath(zip_filename)}")
        
    except Exception as e:
        print(f"\n❌ Failed to create backup: {e}")

if __name__ == "__main__":
    zip_project()
