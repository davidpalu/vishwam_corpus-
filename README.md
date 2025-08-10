# Image Captioning Dataset Builder

A comprehensive Streamlit application for building multilingual image captioning datasets with support for 23+ Indian languages.

## Features

🔥 **Core Functionality:**
- Upload images and add captions in multiple Indian languages
- Random image selection for additional captioning
- Metadata storage in CSV format
- Complete dataset download as ZIP file

📸 **Image Management:**
- Support for PNG, JPG, JPEG, GIF, BMP formats
- Automatic image organization in folders
- Unique filename generation to prevent conflicts

🌐 **Language Support:**
23+ Indian languages including:
- Hindi, Bengali, Telugu, Marathi, Tamil
- Gujarati, Urdu, Kannada, Odia, Malayalam
- Punjabi, Assamese, Sanskrit, Nepali
- And many more regional languages

## Installation

1. Install Python 3.7 or higher
2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the Streamlit app:
```bash
streamlit run image_captioning_app.py
```

2. Open your browser and navigate to the displayed URL (usually http://localhost:8501)

3. Use the sidebar to navigate between different functions:
   - **Upload & Caption Images**: Upload new images and add captions
   - **Caption Random Images**: Add captions to existing images
   - **View Dataset**: See statistics and metadata
   - **Download Dataset**: Get your complete dataset as ZIP

## Dataset Structure

The app creates the following folder structure:
```
├── uploaded_images/          # Original uploaded images
├── captioned_images/         # Images with additional captions
├── metadata/
│   ├── image_metadata.csv    # Metadata for uploaded images
│   └── captioned_metadata.csv # Metadata for captioned images
├── image_captioning_app.py   # Main application
└── requirements.txt          # Dependencies
```

## Metadata Format

Each CSV file contains:
- `filename`: Unique image filename
- `original_name`: Original uploaded filename  
- `caption`: Image caption text
- `language`: Language name (e.g., "Hindi")
- `language_code`: ISO language code (e.g., "hi")
- `timestamp`: When the entry was created
- `file_size`: Image file size (for uploads)

## Supported Languages

The app supports all major Indian languages:
- English (en), Hindi (hi), Bengali (bn), Telugu (te)
- Marathi (mr), Tamil (ta), Gujarati (gu), Urdu (ur)
- Kannada (kn), Odia (or), Malayalam (ml), Punjabi (pa)
- Assamese (as), Maithili (mai), Sanskrit (sa), Nepali (ne)
- Konkani (kok), Manipuri (mni), Bodo (brx), Dogri (doi)
- Kashmiri (ks), Santali (sat), Sindhi (sd)

## Tips for Best Results

1. **Image Quality**: Upload clear, high-quality images for better dataset quality
2. **Caption Quality**: Write descriptive, accurate captions in the target language
3. **Language Consistency**: Try to maintain consistent language usage within the same session
4. **Regular Backups**: Download your dataset regularly to avoid data loss

## Troubleshooting

- **Images not displaying**: Check file format (should be PNG, JPG, JPEG, GIF, or BMP)
- **Download fails**: Ensure you have images in the dataset before downloading
- **App crashes**: Check that all dependencies are installed correctly

## Contributing

Feel free to contribute improvements, bug fixes, or additional language support!
