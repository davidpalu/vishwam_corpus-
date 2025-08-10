# Sample usage script for the Image Captioning Dataset Builder

# This script demonstrates how you might use the dataset created by the app

import pandas as pd
import os
from PIL import Image

def load_dataset():
    """Load the complete dataset created by the Streamlit app"""

    # Load metadata
    metadata_files = []

    if os.path.exists("metadata/image_metadata.csv"):
        df1 = pd.read_csv("metadata/image_metadata.csv")
        df1['source'] = 'uploaded'
        metadata_files.append(df1)

    if os.path.exists("metadata/captioned_metadata.csv"):
        df2 = pd.read_csv("metadata/captioned_metadata.csv") 
        df2['source'] = 'captioned'
        metadata_files.append(df2)

    if metadata_files:
        complete_metadata = pd.concat(metadata_files, ignore_index=True)
        return complete_metadata
    else:
        return pd.DataFrame()

def analyze_dataset():
    """Analyze the dataset and print statistics"""

    df = load_dataset()

    if df.empty:
        print("No dataset found. Please run the Streamlit app first!")
        return

    print("📊 DATASET ANALYSIS")
    print("="*50)
    print(f"Total images: {len(df)}")
    print(f"Unique languages: {df['language'].nunique()}")
    print("\nLanguage distribution:")
    print(df['language'].value_counts())
    print("\nLanguage codes:")
    print(df[['language', 'language_code']].drop_duplicates())

def get_images_by_language(language):
    """Get all images for a specific language"""

    df = load_dataset()

    if df.empty:
        return []

    filtered = df[df['language'] == language]

    images_data = []
    for _, row in filtered.iterrows():
        # Determine which folder to look in
        folder = "uploaded_images" if row['source'] == 'uploaded' else "captioned_images"
        image_path = os.path.join(folder, row['filename'])

        if os.path.exists(image_path):
            images_data.append({
                'path': image_path,
                'caption': row['caption'],
                'filename': row['filename']
            })

    return images_data

# Example usage
if __name__ == "__main__":
    # Analyze the dataset
    analyze_dataset()

    # Get all Hindi images
    hindi_images = get_images_by_language("Hindi")
    print(f"\nFound {len(hindi_images)} Hindi images")

    # Display first few captions
    for i, img_data in enumerate(hindi_images[:3]):
        print(f"Image {i+1}: {img_data['caption']}")
