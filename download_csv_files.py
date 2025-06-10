import gdown
import os

# Create the destination folder if it doesn't exist
os.makedirs('data', exist_ok=True)

# Google Drive folder ID
folder_url = "https://drive.google.com/drive/folders/1q3K5rlruQ46DRIhgbE8c7UkDjhiq0VUG?usp=drive_link"

# Download the entire folder
gdown.download_folder(folder_url, output='data', quiet=False, use_cookies=False)
