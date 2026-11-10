
import streamlit as st
import tempfile
import os
import time

from google import genai


# -------------------------------
# PAGE CONFIGURATION
# -------------------------------

st.set_page_config(
    page_title="AI Helmet Detection",
    page_icon="🪖",
    layout="wide"
)


# -------------------------------
# CUSTOM UI
# -------------------------------

st.title("🪖 AI Helmet & Cap Detection")

st.write(
    "Upload a short video and let AI analyze "
    "visible people and their headwear."
)

st.info(
    "This application analyzes headwear only. "
    "It does not identify people's identities."
)


# -------------------------------
# API KEY
# -------------------------------

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error(
        "Gemini API key not found. "
        "Please configure GEMINI_API_KEY."
    )
    st.stop()

client = genai.Client(api_key=api_key)


# -------------------------------
# VIDEO UPLOAD
# -------------------------------

uploaded_file = st.file_uploader(
    "Upload your video (approximately 20 seconds)",
    type=["mp4", "mov", "avi", "webm"]
)

if uploaded_file:

    st.subheader("Video Preview")

    st.video(uploaded_file)

    st.write("File:", uploaded_file.name)

    st.write(
        f"Size: {uploaded_file.size / (1024 * 1024):.2f} MB"
    )

    if uploaded_file.size > 100 * 1024 * 1024:
        st.error("Please upload a video smaller than 100 MB.")

    elif st.button("🔍 Analyze Video", type="primary"):

        temp_path = None

        try:

            with st.spinner(
                "Uploading video to Gemini..."
            ):

                suffix = os.path.splitext(
                    uploaded_file.name
                )[1]

                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=suffix
                ) as temp_file:

                    temp_file.write(
                        uploaded_file.getvalue()
                    )

                    temp_path = temp_file.name

                video_file = client.files.upload(
                    file=temp_path
                )

            # Wait for video processing

            progress = st.progress(0)

            for attempt in range(120):

                video_file = client.files.get(
                    name=video_file.name
                )

                state = video_file.state.name

                if state == "ACTIVE":
                    progress.progress(100)
                    break

                if state == "FAILED":
                    raise RuntimeError(
                        "Gemini could not process the video."
                    )

                progress.progress(
                    min(95, int((attempt + 1) / 120 * 100))
                )

                time.sleep(2)

            else:
                raise TimeoutError(
                    "Video processing timed out."
                )

            # AI ANALYSIS PROMPT

            prompt = """
            Analyze this video for visible people and
            their headwear.

            Report only visual observations.

            For each distinguishable person, provide:

            1. A temporary visual label such as Person 1.
            2. Approximate timestamp.
            3. Whether the person appears to wear:
               - Safety helmet / hard hat
               - Ordinary cap
               - No visible headwear
               - Unclear / not visible

            Do not guess when the head is obscured,
            too small, or outside the frame.

            Explain that a normal cap is not a safety helmet.

            Give an approximate count of visible people,
            but do not count the same person repeatedly
            when they appear across multiple frames.

            Do not identify anyone by name or identity.

            Present the findings in a clear table,
            followed by a short summary.

            Mention that this is an AI visual estimate,
            not a certified safety inspection.
            """

            # SEND VIDEO TO GEMINI

            with st.spinner(
                "AI is analyzing the video..."
            ):

                response = client.interactions.create(
                    model="gemini-3.8-flash",
                    input=[
                        {
                            "type": "video",
                            "uri": video_file.uri,
                            "mime_type": video_file.mime_type,
                            "processing": "static"
                        },
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ]
                )

            # DISPLAY RESULTS

            st.success("Analysis completed!")

            st.subheader("📊 Detection Results")

            st.markdown(response.output_text)

        except Exception as e:

            st.error(
                f"Analysis failed: {str(e)}"
            )

        finally:

            if temp_path and os.path.exists(temp_path):
                os.remove(temp_path)

else:

    st.warning(
        "Please upload a video to begin."
    )


# -------------------------------
# FOOTER
# -------------------------------

st.divider()

st.caption(
    "AI Helmet Detection | Python | Streamlit | Gemini API"
)
