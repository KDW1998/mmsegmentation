import os
import numpy as np
import argparse
from PIL import Image
import shutil

def parse_args():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--srx_dir', help='the root directory that contains gtFine and leftImg8bit folders')
    args = parser.parse_args()
    return args

args = parse_args()
data_root = args.srx_dir
gtFine_folder = os.path.join(data_root, 'gtFine')
leftImg8bit_folder = os.path.join(data_root, 'leftImg8bit')

# Create new folders to store images that do not contain the value 1
new_folder = os.path.join(data_root, 'new_folder')
os.makedirs(new_folder, exist_ok=True)
new_gtFine_folder = os.path.join(new_folder, 'gtFine')
new_leftImg8bit_folder = os.path.join(new_folder, 'leftImg8bit')
os.makedirs(new_gtFine_folder, exist_ok=True)
os.makedirs(new_leftImg8bit_folder, exist_ok=True)

# Function to process each image
def process_images(gtFine_folder, leftImg8bit_folder, new_gtFine_folder, new_leftImg8bit_folder):
    for dirpath, dirnames, filenames in os.walk(gtFine_folder):
        relative_dirpath = os.path.relpath(dirpath, gtFine_folder)
        
        structure_gtFine = os.path.join(new_gtFine_folder, relative_dirpath)
        os.makedirs(structure_gtFine, exist_ok=True)

        structure_leftImg8bit = os.path.join(new_leftImg8bit_folder, relative_dirpath)
        os.makedirs(structure_leftImg8bit, exist_ok=True)

        for file_name in filenames:
            if file_name.endswith("_gtFine_labelIds.png"):  # Check if the file is a .png file
                old_file_path_gtFine = os.path.join(dirpath, file_name)
                
                # Load the .png file as a numpy array
                img = Image.open(old_file_path_gtFine)
                data = np.array(img)
                
                # Check if 1 exists in the numpy array
                if not np.any(data == 1):
                    print(f"Copying {file_name}")
                    # Copy the gtFine file to the new folder
                    new_file_path_gtFine = os.path.join(structure_gtFine, file_name)
                    shutil.copy(old_file_path_gtFine, new_file_path_gtFine)

                    # Copy the corresponding leftImg8bit file to the new folder
                    leftImg8bit_file_name = file_name.replace("_gtFine_labelIds.png", "_leftImg8bit.png")
                    old_file_path_leftImg8bit = os.path.join(leftImg8bit_folder, relative_dirpath, leftImg8bit_file_name)
                    if os.path.exists(old_file_path_leftImg8bit):
                        new_file_path_leftImg8bit = os.path.join(structure_leftImg8bit, leftImg8bit_file_name)
                        shutil.copy(old_file_path_leftImg8bit, new_file_path_leftImg8bit)
                        print(f"Also copied corresponding {leftImg8bit_file_name}")
                else:
                    print(f"1s found in {file_name}. File not copied.")



# Process images in the gtFine folder and the leftImg8bit folder
process_images(gtFine_folder, leftImg8bit_folder, new_gtFine_folder, new_leftImg8bit_folder)
