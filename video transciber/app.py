import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from googletrans import Translator

def get_video_id(url):
    """Extract YouTube video ID from the given URL."""
    try:
        if "v=" in url:
            return url.split("v=")[1].split("&")[0]
        elif "youtu.be/" in url:
            return url.split("youtu.be/")[1]
        else:
            return None
    except Exception as e:
        return None

def fetch_transcript(video_id, language='en'):
    """Fetch transcript from YouTube video."""
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[language])
        return " ".join([item['text'] for item in transcript])
    except Exception as e:
        return None

def translate_text(text, target_language):
    """Translate text to the target language."""
    translator = Translator()
    return translator.translate(text, dest=target_language).text

def main():
    st.set_page_config(page_title="YouTube Video to Text", page_icon="🔤", layout="wide")

    # Header
    st.markdown(
        """<h1 style='text-align: center; color: #FF6347;'>YouTube Video to Text</h1>""",
        unsafe_allow_html=True,
    )

    st.markdown(
        """<h3 style='text-align: center; color: #4682B4;'>Extract text from YouTube videos in English, Hindi, or Telugu</h3>""",
        unsafe_allow_html=True,
    )

    # Input Section
    st.write("### Enter the YouTube Video Link")
    video_url = st.text_input("Paste your YouTube video link here:")

    st.write("### Select Language for the Text")
    language_options = {
        "English": "en",
        "Hindi": "hi",
        "Telugu": "te"
    }
    language = st.selectbox("Choose language:", options=list(language_options.keys()))

    # Submit Button
    if st.button("Get Text"):
        if not video_url:
            st.error("Please provide a valid YouTube video link.")
        else:
            video_id = get_video_id(video_url)
            if video_id:
                st.info("Processing the video, please wait...")
                original_text = fetch_transcript(video_id, language='en')

                if original_text:
                    if language_options[language] != 'en':
                        translated_text = translate_text(original_text, language_options[language])
                        st.write(f"### Translated Text in {language}")
                        st.text_area("", value=translated_text, height=300)
                    else:
                        st.write("### Extracted Text")
                        st.text_area("", value=original_text, height=300)
                else:
                    st.error("Unable to fetch the transcript. Please check if the video has captions enabled.")
            else:
                st.error("Invalid YouTube URL. Please try again.")

    # Footer
    st.markdown(
        """<h6 style='text-align: center; color: #808080;'>Developed with ❤️ by Streamlit Enthusiasts</h6>""",
        unsafe_allow_html=True,
    )

if __name__ == "__main__":
    main()
