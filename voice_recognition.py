import streamlit as st
import speech_recognition as sr
import os
from io import BytesIO
import wave
import uuid
from datetime import datetime
import sounddevice as sd
import soundfile as sf


class SpeechRecognizer:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        # Ensure voice input directory exists
        if not os.path.exists("voice_inputs"):
            os.makedirs("voice_inputs")

    def adjust_for_ambient_noise(self):
        """No-op when using sounddevice for recording (kept for API compatibility)"""
        return

    def record_with_sounddevice(self, duration_seconds: int = 10, samplerate: int = 16000, channels: int = 1):
        """Record audio using sounddevice and save as 16-bit PCM WAV. Returns (filepath, duration)."""
        try:
            st.info(f"🎙️ Recording for {duration_seconds} seconds...")
            recording = sd.rec(int(duration_seconds * samplerate), samplerate=samplerate, channels=channels, dtype='int16')
            sd.wait()

            unique_id = uuid.uuid4()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"voice_{timestamp}_{unique_id}.wav"
            filepath = os.path.join("voice_inputs", filename)
            # Write WAV
            sf.write(filepath, recording, samplerate, subtype='PCM_16')
            return filepath, float(duration_seconds)
        except Exception as e:
            st.error(f"Error recording audio: {str(e)}")
            return None, None

    def recognize_speech(self, audio, language='en-US'):
        """Convert audio to text using Google Speech Recognition (simple)"""
        try:
            text = self.recognizer.recognize_google(audio, language=language)
            return text
        except sr.UnknownValueError:
            return "Could not understand audio"
        except sr.RequestError as e:
            return f"Error with speech recognition service: {str(e)}"
        except Exception as e:
            return f"Error recognizing speech: {str(e)}"

    def recognize_with_details(self, audio, language='en-US'):
        """Recognize speech and return transcript, confidence, and raw result."""
        try:
            raw = self.recognizer.recognize_google(audio, language=language, show_all=True)
            transcript = ""
            confidence = None
            if isinstance(raw, dict):
                alternatives = raw.get('alternative', [])
                if alternatives:
                    transcript = alternatives[0].get('transcript', '')
                    confidence = alternatives[0].get('confidence')
            # Fallback to simple recognition if needed
            if not transcript:
                transcript = self.recognizer.recognize_google(audio, language=language)
            return {
                'transcript': transcript,
                'confidence': confidence,
                'raw': raw
            }
        except sr.UnknownValueError:
            return {
                'transcript': "",
                'confidence': None,
                'raw': {'error': 'unknown_value'}
            }
        except sr.RequestError as e:
            return {
                'transcript': "",
                'confidence': None,
                'raw': {'error': f'request_error: {str(e)}'}
            }
        except Exception as e:
            return {
                'transcript': "",
                'confidence': None,
                'raw': {'error': f'exception: {str(e)}'}
            }

    def load_audio_for_recognition(self, wav_path: str):
        """Load a WAV file into sr.AudioData for recognition."""
        try:
            with sr.AudioFile(wav_path) as source:
                audio = self.recognizer.record(source)
            return audio
        except Exception as e:
            st.error(f"Error loading audio for recognition: {str(e)}")
            return None

    def get_language_code(self, language_name):
        """Convert language name to speech recognition language code"""
        language_codes = {
            "English": "en-US",
            "Hindi": "hi-IN",
            "Bengali": "bn-IN",
            "Telugu": "te-IN",
            "Marathi": "mr-IN",
            "Tamil": "ta-IN",
            "Gujarati": "gu-IN",
            "Urdu": "ur-IN",
            "Kannada": "kn-IN",
            "Odia": "or-IN",
            "Malayalam": "ml-IN",
            "Punjabi": "pa-IN",
            "Assamese": "as-IN",
            "Nepali": "ne-NP",
            "Sanskrit": "sa-IN",
        }
        return language_codes.get(language_name, "en-US")


def create_voice_input_component(language="English", key_suffix=""):
    """Create a voice input component for Streamlit"""

    # Initialize speech recognizer
    if f'speech_recognizer_{key_suffix}' not in st.session_state:
        st.session_state[f'speech_recognizer_{key_suffix}'] = SpeechRecognizer()

    recognizer = st.session_state[f'speech_recognizer_{key_suffix}']

    # Voice input section
    st.markdown("### 🎤 Voice Input")

    col1, col2 = st.columns([1, 1])

    with col1:
        duration = st.slider("Recording duration (seconds)", min_value=3, max_value=30, value=10, key=f"duration_{key_suffix}")
        if st.button("🎤 Record", key=f"record_{key_suffix}", type="primary"):
            with st.spinner("🎧 Recording and processing..."):
                # Record to WAV using sounddevice
                audio_path, audio_duration = recognizer.record_with_sounddevice(duration_seconds=duration)
                if audio_path:
                    st.session_state[f'voice_audio_path_{key_suffix}'] = audio_path
                    st.session_state[f'voice_audio_duration_{key_suffix}'] = audio_duration
                    # Get language code
                    lang_code = recognizer.get_language_code(language)
                    # Load for recognition
                    audio_data = recognizer.load_audio_for_recognition(audio_path)
                    if audio_data is not None:
                        result = recognizer.recognize_with_details(audio_data, language=lang_code)
                        transcript = result.get('transcript', '')
                        confidence = result.get('confidence')
                        raw = result.get('raw')

                        st.session_state[f'voice_text_{key_suffix}'] = transcript
                        st.session_state[f'voice_confidence_{key_suffix}'] = confidence
                        st.session_state[f'voice_raw_{key_suffix}'] = raw
                        st.session_state[f'voice_language_code_{key_suffix}'] = lang_code
                        st.session_state[f'voice_provider_{key_suffix}'] = 'google_speech_recognition'

                        if not transcript:
                            st.error("❌ Could not understand audio or recognition failed")
                        else:
                            st.success("✅ Speech recognized successfully!")
                else:
                    st.warning("⚠️ Recording failed. Please try again.")

    with col2:
        # Clear button
        if st.button("🗑️ Clear", key=f"clear_{key_suffix}"):
            if f'voice_text_{key_suffix}' in st.session_state:
                del st.session_state[f'voice_text_{key_suffix}']
            st.success("✅ Voice input cleared!")

    # Display recognized text
    if f'voice_text_{key_suffix}' in st.session_state:
        recognized_text = st.session_state[f'voice_text_{key_suffix}']

        if not ("Could not understand" in recognized_text or "Error" in recognized_text):
            st.markdown("### 📝 Recognized Text")

            # Editable text area with recognized text
            edited_text = st.text_area(
                f"Edit caption in {language}",
                value=recognized_text,
                height=150,
                key=f"edit_text_{key_suffix}",
                help=f"You can edit the recognized text or use it as is",
            )

            return edited_text
        else:
            st.error(f"❌ {recognized_text}")
            return ""

    return ""


def install_speech_dependencies():
    """Check presence of required dependencies for voice capture and recognition"""
    try:
        import sounddevice  # noqa: F401
        import soundfile  # noqa: F401
        import speech_recognition  # noqa: F401
        return True
    except ImportError:
        return False

