import os
import shutil
import time
import sys
sys.path.append(r'C:\Users\Dor Shukrun\AllCoding\Exelanteam\Klaido\kaleidoo-team_6')

from doc_extraction.extractor import save_text_to_file


def check_and_process_files(src_folder, dest_folder, process_file, fixed_dest_folder):
    while True:
        # List files in the source folder
        files = os.listdir(src_folder)
        
        if files:
            # Get the first file in the folder
            file_path = os.path.join(src_folder, files[0])
            
            try:
                # Ensure the destination folders exist
                if not os.path.exists(dest_folder):
                    os.makedirs(dest_folder)
                if not os.path.exists(fixed_dest_folder):
                    os.makedirs(fixed_dest_folder)
                
                # Process the file using the provided function
                process_file(file_path, fixed_dest_folder)
                
                # Move the file to the destination folder if processing is successful
                shutil.move(file_path, dest_folder)
                print(f"{file_path} has been moved to the destination folder")
                
            except Exception as e:
                print(f"Error processing the file {file_path}: {e}")
                
        # Wait for 3 seconds before the next check
        time.sleep(3)


if __name__ == "__main__":
    # Define source and destination paths
    src = r'doc_extraction\data\unprocessed_files'
    dest = r'doc_extraction\data\extracted_files'
    fixed_dest_folder = r"doc_extraction\data\fixed_files"
    
    # Start the file processing function
    check_and_process_files(src, dest, save_text_to_file, fixed_dest_folder)
