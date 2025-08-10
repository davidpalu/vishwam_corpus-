# Let me create a comprehensive Streamlit application as requested
# First, let's create the basic structure and code for the application

streamlit_app_code = '''
import streamlit as st
import os
import pandas as pd
import zipfile
import io
import random
from PIL import Image
import uuid
from datetime import datetime

# Indian languages with their codes
INDIAN_LANGUAGES = {
    "English": "en",
    "Hindi": "hi",
    "Bengali": "bn", 
    "Telugu": "te",
    "Marathi": "mr",
    "Tamil": "ta",
    "Gujarati": "gu",
    "Urdu": "ur",
    "Kannada": "kn",
    "Odia": "or",
    "Malayalam": "ml",
    "Punjabi": "pa",
    "Assamese": "as",
    "Maithili": "mai",
    "Sanskrit": "sa",
    "Nepali": "ne",
    "Konkani": "kok",
    "Manipuri": "mni",
    "Bodo": "brx",
    "Dogri": "doi",
    "Kashmiri": "ks",
    "Santali": "sat",
    "Sindhi": "sd"
}

def initialize_directories():
    """Create necessary directories if they don't exist"""
    directories = ["uploaded_images", "captioned_images", "metadata"]
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)

def save_image_and_metadata(uploaded_file, caption, language):
    """Save uploaded image and its metadata"""
    initialize_directories()
    
    # Generate unique filename
    file_extension = uploaded_file.name.split('.')[-1]
    unique_filename = f"{uuid.uuid4()}.{file_extension}"
    
    # Save image
    image_path = os.path.join("uploaded_images", unique_filename)
    with open(image_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Save metadata
    metadata = {
        "filename": unique_filename,
        "original_name": uploaded_file.name,
        "caption": caption,
        "language": language,
        "language_code": INDIAN_LANGUAGES[language],
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "file_size": uploaded_file.size
    }
    
    # Load existing metadata or create new
    metadata_file = "metadata/image_metadata.csv"
    if os.path.exists(metadata_file):
        df = pd.read_csv(metadata_file)
        df = pd.concat([df, pd.DataFrame([metadata])], ignore_index=True)
    else:
        df = pd.DataFrame([metadata])
    
    df.to_csv(metadata_file, index=False)
    
    return unique_filename

def get_random_image():
    """Get a random image from uploaded_images folder"""
    initialize_directories()
    
    if not os.path.exists("uploaded_images"):
        return None
    
    images = [f for f in os.listdir("uploaded_images") if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
    
    if not images:
        return None
    
    return random.choice(images)

def save_captioned_image(filename, caption, language):
    """Save image with new caption to captioned_images folder"""
    initialize_directories()
    
    # Copy image to captioned folder
    src_path = os.path.join("uploaded_images", filename)
    dst_path = os.path.join("captioned_images", filename)
    
    if os.path.exists(src_path):
        # Copy the file
        with open(src_path, "rb") as src_file:
            with open(dst_path, "wb") as dst_file:
                dst_file.write(src_file.read())
        
        # Update metadata
        metadata = {
            "filename": filename,
            "caption": caption,
            "language": language,
            "language_code": INDIAN_LANGUAGES[language],
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "captioned"
        }
        
        # Save captioned metadata
        captioned_metadata_file = "metadata/captioned_metadata.csv"
        if os.path.exists(captioned_metadata_file):
            df = pd.read_csv(captioned_metadata_file)
            df = pd.concat([df, pd.DataFrame([metadata])], ignore_index=True)
        else:
            df = pd.DataFrame([metadata])
        
        df.to_csv(captioned_metadata_file, index=False)
        
        return True
    return False

def create_dataset_zip():
    """Create a zip file containing all images and metadata"""
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        # Add uploaded images
        if os.path.exists("uploaded_images"):
            for filename in os.listdir("uploaded_images"):
                file_path = os.path.join("uploaded_images", filename)
                zip_file.write(file_path, f"uploaded_images/{filename}")
        
        # Add captioned images
        if os.path.exists("captioned_images"):
            for filename in os.listdir("captioned_images"):
                file_path = os.path.join("captioned_images", filename)
                zip_file.write(file_path, f"captioned_images/{filename}")
        
        # Add metadata files
        if os.path.exists("metadata"):
            for filename in os.listdir("metadata"):
                if filename.endswith('.csv'):
                    file_path = os.path.join("metadata", filename)
                    zip_file.write(file_path, f"metadata/{filename}")
    
    zip_buffer.seek(0)
    return zip_buffer.getvalue()

def main():
    st.set_page_config(
        page_title="Image Captioning Dataset Builder",
        page_icon="📸",
        layout="wide"
    )
    
    st.title("📸 Image Captioning Dataset Builder")
    st.markdown("Build your multilingual image captioning dataset with support for Indian languages!")
    
    # Initialize directories
    initialize_directories()
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    tab = st.sidebar.radio("Choose Action", [
        "Upload & Caption Images", 
        "Caption Random Images", 
        "View Dataset", 
        "Download Dataset"
    ])
    
    if tab == "Upload & Caption Images":
        st.header("📤 Upload & Caption Images")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # Image upload
            uploaded_file = st.file_uploader(
                "Choose an image file", 
                type=['png', 'jpg', 'jpeg', 'gif', 'bmp'],
                help="Upload an image to add to your dataset"
            )
            
            if uploaded_file is not None:
                # Display uploaded image
                image = Image.open(uploaded_file)
                st.image(image, caption="Uploaded Image", use_column_width=True)
        
        with col2:
            if uploaded_file is not None:
                # Language selection
                selected_language = st.selectbox(
                    "Select Language for Caption",
                    options=list(INDIAN_LANGUAGES.keys()),
                    index=0,
                    help="Choose the language for your image caption"
                )
                
                # Caption input
                caption = st.text_area(
                    f"Enter caption in {selected_language}",
                    height=150,
                    help=f"Provide a descriptive caption in {selected_language}"
                )
                
                # Save button
                if st.button("💾 Save Image & Caption", type="primary"):
                    if caption.strip():
                        filename = save_image_and_metadata(uploaded_file, caption, selected_language)
                        st.success(f"✅ Image saved successfully as {filename}")
                        st.success(f"📝 Caption: {caption}")
                        st.success(f"🌐 Language: {selected_language}")
                    else:
                        st.error("Please enter a caption before saving!")
    
    elif tab == "Caption Random Images":
        st.header("🎲 Caption Random Images")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            if st.button("🎲 Get Random Image", type="primary"):
                random_image = get_random_image()
                if random_image:
                    st.session_state.random_image = random_image
                else:
                    st.warning("No images found! Please upload some images first.")
            
            if "random_image" in st.session_state:
                image_path = os.path.join("uploaded_images", st.session_state.random_image)
                if os.path.exists(image_path):
                    image = Image.open(image_path)
                    st.image(image, caption=f"Random Image: {st.session_state.random_image}", use_column_width=True)
        
        with col2:
            if "random_image" in st.session_state:
                # Language selection for captioning
                selected_language = st.selectbox(
                    "Select Language for New Caption",
                    options=list(INDIAN_LANGUAGES.keys()),
                    index=0,
                    key="caption_language"
                )
                
                # Caption input
                new_caption = st.text_area(
                    f"Enter new caption in {selected_language}",
                    height=150,
                    key="new_caption"
                )
                
                # Save caption button
                if st.button("💾 Save Caption", type="primary"):
                    if new_caption.strip():
                        success = save_captioned_image(
                            st.session_state.random_image, 
                            new_caption, 
                            selected_language
                        )
                        if success:
                            st.success("✅ Caption saved successfully!")
                            st.success(f"📝 Caption: {new_caption}")
                            st.success(f"🌐 Language: {selected_language}")
                            # Clear the random image to get a new one
                            del st.session_state.random_image
                        else:
                            st.error("Error saving caption!")
                    else:
                        st.error("Please enter a caption before saving!")
    
    elif tab == "View Dataset":
        st.header("👁️ View Dataset")
        
        # Show statistics
        col1, col2, col3, col4 = st.columns(4)
        
        uploaded_count = len([f for f in os.listdir("uploaded_images") if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]) if os.path.exists("uploaded_images") else 0
        captioned_count = len([f for f in os.listdir("captioned_images") if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]) if os.path.exists("captioned_images") else 0
        
        with col1:
            st.metric("📤 Uploaded Images", uploaded_count)
        
        with col2:
            st.metric("📝 Captioned Images", captioned_count)
        
        with col3:
            st.metric("📊 Total Images", uploaded_count + captioned_count)
        
        with col4:
            # Count unique languages
            unique_languages = set()
            if os.path.exists("metadata/image_metadata.csv"):
                df = pd.read_csv("metadata/image_metadata.csv")
                unique_languages.update(df['language'].unique())
            if os.path.exists("metadata/captioned_metadata.csv"):
                df = pd.read_csv("metadata/captioned_metadata.csv")
                unique_languages.update(df['language'].unique())
            st.metric("🌐 Languages", len(unique_languages))
        
        # Show metadata tables
        st.subheader("📊 Dataset Metadata")
        
        tab1, tab2 = st.tabs(["Uploaded Images", "Captioned Images"])
        
        with tab1:
            if os.path.exists("metadata/image_metadata.csv"):
                df = pd.read_csv("metadata/image_metadata.csv")
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No uploaded images metadata found.")
        
        with tab2:
            if os.path.exists("metadata/captioned_metadata.csv"):
                df = pd.read_csv("metadata/captioned_metadata.csv")
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No captioned images metadata found.")
    
    elif tab == "Download Dataset":
        st.header("📥 Download Dataset")
        
        st.markdown("""
        Download your complete image captioning dataset including:
        - **Uploaded Images**: Original images with captions
        - **Captioned Images**: Images with additional captions  
        - **Metadata**: CSV files containing all caption and language information
        """)
        
        # Show dataset summary
        uploaded_count = len([f for f in os.listdir("uploaded_images") if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]) if os.path.exists("uploaded_images") else 0
        captioned_count = len([f for f in os.listdir("captioned_images") if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]) if os.path.exists("captioned_images") else 0
        
        if uploaded_count > 0 or captioned_count > 0:
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.info(f"📊 **Dataset Summary:**\\n- {uploaded_count} uploaded images\\n- {captioned_count} captioned images\\n- {uploaded_count + captioned_count} total images")
            
            with col2:
                # Create download button
                zip_data = create_dataset_zip()
                
                st.download_button(
                    label="📥 Download Complete Dataset (ZIP)",
                    data=zip_data,
                    file_name=f"image_dataset_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip",
                    mime="application/zip",
                    type="primary"
                )
                
                st.success("✅ Click the button above to download your dataset!")
        else:
            st.warning("⚠️ No images found in the dataset. Please upload some images first!")
    
    # Footer
    st.markdown("---")
    st.markdown("Built with ❤️ using Streamlit | Support for 23+ Indian Languages")

if __name__ == "__main__":
    main()
'''

print("Streamlit application code created successfully!")
print("\\nKey Features:")
print("1. ✅ Image upload with caption input")
print("2. ✅ Language selection (23+ Indian languages + English)")
print("3. ✅ Random image selection for captioning")
print("4. ✅ Metadata storage in CSV format") 
print("5. ✅ ZIP download functionality")
print("6. ✅ Dataset viewing and statistics")

# Save the code to a file
with open('image_captioning_app.py', 'w', encoding='utf-8') as f:
    f.write(streamlit_app_code)

print("\\n📁 File saved as: image_captioning_app.py")
print("\\n🚀 To run the app:")
print("   streamlit run image_captioning_app.py")