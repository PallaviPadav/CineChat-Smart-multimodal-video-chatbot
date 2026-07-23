import streamlit as st
from pathlib import Path
import re
import requests
import base64
from Code.Data_ingesion.fetch_video import download_video 
from Code.main import process_video, ask_question
from Code.model.summarizer import get_summary
from config import config
from Code.utils.logger import get_logger
logger = get_logger(__name__)

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title=" CineChat 🎧",
    page_icon="🎧",
    layout="wide"
)

# =========================================================
# BACKGROUND IMAGE
# =========================================================
path_theme = Path("Artifacts/Theme.PNG")


def get_base64_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()


img_base64 = get_base64_image(path_theme)

# =========================================================
# CSS (BLUR + DARK OVERLAY)
# =========================================================
st.markdown(f"""
<style>

/* =========================================================
   BACKGROUND IMAGE
   ========================================================= */
.stApp {{
    background-image: url("data:image/png;base64,{img_base64}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}

/* =========================================================
   DARK GLASS OVERLAY
   ========================================================= */
.stApp::before {{
    content: "";
    position: fixed;
    inset: 0;

    background: rgba(0, 0, 0, 0.55);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);

    z-index: 0;
}}

/* =========================================================
   KEEP STREAMLIT CONTENT ABOVE OVERLAY
   ========================================================= */
.block-container {{
    position: relative;
    z-index: 1;
    padding-top: 1rem;
    padding-bottom: 1rem;
}}

/* =========================================================
   GLASS PANEL
   ========================================================= */
.glass-container {{
    max-width: 1400px;
    margin: auto;
    padding: 25px;

    background: rgba(255,255,255,0.18);
    backdrop-filter: blur(22px);
    -webkit-backdrop-filter: blur(22px);

    border-radius: 25px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.35);
    border: 1px solid rgba(255,255,255,0.15);
}}

/* =========================================================
   TITLE
   ========================================================= */
.title {{
    text-align: center;
    font-size: 68px;
    font-weight: 900;
    color: white;
    text-shadow: 2px 2px 15px black;
}}

.subtitle {{
    text-align: center;
    font-size: 26px;
    color: white;
    margin-bottom: 20px;
    font-weight: bold;
}}

/* =========================================================
   BUTTONS
   ========================================================= */



/* Start button */

div.stButton > button {{
    width: 100%;
    min-height: 70px ;
    border-radius: 12px ;
    background: linear-gradient(90deg, #ff512f, #dd2476) ;
    color: black ;
    border: none ;
}}

/* Button label */
div.stButton > button * {{
    font-size: 28px ;
    font-weight: 900 ;
    color: black ;
}}

/* Hover */
div.stButton > button:hover {{
    transform: scale(1.03);
    background: linear-gradient(90deg, #24c6dc, #514a9d) ;
}}

/* =========================================================
   INPUT BOXES
   ========================================================= */
.stTextInput input {{
    background: rgba(255,255,255,0.95);
    color: black;
    border-radius: 10px;
}}


# =========================================================
#   LEFT PANEL
#   ========================================================= */

.video-title{{
    font-size:40px;
    font-weight:900;
    color:black;
    margin-bottom:12px;
}}

.url-label{{
    font-size:26px;
    font-weight:900;
    color:black;
    margin-bottom:8px;
}}

/* Text input */
div[data-testid="stTextInput"] input{{
    height:70px !important;
    font-size:22px !important;
    font-weight:700 !important;
    color:black !important;
    background:white !important;
    border:2px solid #514a9d !important;
    border-radius:12px !important;
}}

/* Placeholder */
div[data-testid="stTextInput"] input::placeholder{{
    font-size:20px !important;
    color:#555 !important;
}}

/* Success/Error/Info */
div[data-testid="stAlert"]{{
    font-size:22px !important;
    font-weight:800 !important;
    color:black !important;
}}

/* Spinner */
div[data-testid="stSpinner"] p{{
    font-size:28px !important;
    font-weight:900 !important;
    color:black !important;
}}

/* Button */
div.stButton > button{{
    font-size:26px !important;
    font-weight:900 !important;
    color:black !important;
    height:70px !important;
}}

/* General markdown text */
div[data-testid="stMarkdownContainer"]{{
    color:black !important;
    font-size:20px;
}}


#=========================================================
#   CHAT AREA
#========================================================= */

# Chat container 
div[data-testid="stChatMessage"]{{
    background: rgba(255,255,255,0.96) !important;
    border-radius:18px !important;
    padding:18px !important;
    margin-bottom:18px !important;
    border:2px solid #d8d8d8;
    box-shadow:0 3px 12px rgba(0,0,0,0.10);
}}

## Chat text 
div[data-testid="stChatMessage"] p,
div[data-testid="stChatMessage"] li,
div[data-testid="stChatMessage"] span{{
    font-size:22px !important;
    font-weight:600 !important;
    color:#000000 !important;
    line-height:1.7;
}}

# Chat markdown 
div[data-testid="stChatMessage"] div[data-testid="stMarkdownContainer"]{{
    color:#000000 !important;
    font-size:22px !important;
}}

# User message 
div[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-user"]){{
    background:#E8F4FF !important;
}}

# Assistant message 
div[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-assistant"]){{
    background:#FFFDEB !important;
}}

/* Entire text input widget */
div[data-testid="stTextInput"]{{
    width:100%;
}}

/* Wrapper */
div[data-testid="stTextInput"] > div{{
    min-height:75px !important;
}}

/* Input container */
div[data-testid="stTextInput"] > div > div{{
    min-height:75px !important;
    border-radius:15px !important;
}}

/* Actual input */
div[data-testid="stTextInput"] input{{
    font-size:24px !important;
    font-weight:700 !important;
    color:black !important;
    background:white !important;
    padding:20px !important;
}}

/* Placeholder */
div[data-testid="stTextInput"] input::placeholder{{
    font-size:22px !important;
}}


# =========================================================
#   OUTPUT CARD
#   ========================================================= */

.output-card{{
    background: rgba(255,255,255,0.95);
    border-radius:18px;
    padding:20px;
    margin-top:15px;
    color:black !important;
    box-shadow:0 5px 18px rgba(0,0,0,.25);
}}

# Summary text */

.summary-text{{
    color:black !important;
    font-size:20px;
    line-height:1.8;
    font-weight:500;
}}

# Status Messages */

.success-box{{
    background:#E8F8EC;
    border-left:6px solid green;
    color:black;
    padding:15px;
    border-radius:12px;
    font-size:20px;
    font-weight:600;
}}

.info-box{{
    background:#EEF5FF;
    border-left:6px solid #2979FF;
    color:black;
    padding:15px;
    border-radius:12px;
    font-size:20px;
    font-weight:600;
}}

# Chat bubbles */

.user-bubble{{

    background:#D7EBFF;
    color:blue;
    padding:22px;
    border-radius:18px;
    font-size:19px;
    margin-bottom:15px;
}}

.bot-bubble{{

    background:#FFF7DA;
    color:blue;
    padding:22px;
    border-radius:18px;
    font-size:19px;
    margin-bottom:15px;
}}

.summary-text {{
    color: white !important;
    font-size: 20px !important;
    font-weight: 700;
    line-height: 2;
    text-align: justify;
    font-family: "Segoe UI", sans-serif;
}}

</style>
""", unsafe_allow_html=True)


# =========================================================
# TITLE
# =========================================================
st.markdown(
    '<div class="title">🎧 CineChat</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">Turn videos into intelligent conversations 🚀</div>',
    unsafe_allow_html=True,
)

# =========================================================
# VALIDATION
# =========================================================
def is_valid_format(link):
    pattern = r"^(https?:\/\/)?(www\.)?(youtube\.com|youtu\.be|vimeo\.com)\/.+"
    return re.match(pattern, link)


def link_exists(url):
    try:
        r = requests.head(url, allow_redirects=True, timeout=5)
        return r.status_code == 200
    except:
        return False


# =========================================================
# SESSION STATE
# =========================================================
if "video_loaded" not in st.session_state:
    st.session_state.video_loaded = False

if "video_path" not in st.session_state:
    st.session_state.video_path = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "summary" not in st.session_state:
    st.session_state.summary = ""


# =========================================================
# MAIN CONTAINER
# =========================================================
st.markdown('<div class="glass-container">', unsafe_allow_html=True)

# Smaller left panel
#left_col, right_col = st.columns([0.8, 2.4], gap="medium")
left_col, summary_col, right_col = st.columns(
    [1.2, 1.0, 1.8],
    gap="medium"
)



# =========================================================
# LEFT PANEL
# =========================================================
with left_col:

    st.markdown(
        '<div class="video-title">🎥 Video</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="url-label">YouTube URL</div>',
        unsafe_allow_html=True
    )

    video_link = st.text_input(
        "YouTube URL",
        placeholder="Paste YouTube link here...",
        key="video_link",
        label_visibility="collapsed"
    )

    if st.button(
        "🚀 Start CineChat",
        use_container_width=True
    ):

        if video_link.strip() == "":
            st.error("Please enter a YouTube URL.")

        elif not is_valid_format(video_link):
            st.error("Invalid YouTube URL.")

        elif not link_exists(video_link):
            st.error("Video cannot be reached.")

        else:

            # -------------------------
            # Download video
            # -------------------------
            with st.spinner("⬇️ Downloading video..."):

                video_path = download_video(video_link)

            if not video_path:
                st.error("Video download failed.")
                st.stop()

            st.session_state.video_loaded = True
            st.session_state.video_path = video_path

            st.success("✅ Video downloaded successfully.")

            # -------------------------
            # Process video
            # -------------------------
            with st.spinner("🎬 Processing video. Please wait..."):

                process_video(video_link)

            st.success("🎉 CineChat is ready!")

    # ----------------------------------------------------
    # Show video only ONCE
    # ----------------------------------------------------
    if (
        st.session_state.get("video_loaded", False)
        and st.session_state.get("video_path")
        and Path(st.session_state.video_path).exists()
    ):

        st.video(
            st.session_state.video_path,
            autoplay=False
        )
    
# =========================================================
# SUMMARY COLUMN
# =========================================================

with summary_col:

    st.markdown("## 📝 Video Summary")
    config.SUMMARY_FLAG = True

    if st.session_state.video_loaded:

        if st.button(
            "📄 Summarize Video",
            use_container_width=True
        ):

            with st.spinner("Generating summary..."):

                summary = get_summary()

            st.session_state.summary = summary

        if st.session_state.get("summary"):


            st.markdown(
                f"""
                <div class="output-card">
                    <div class="summary-text">
                        {st.session_state.summary}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    else:
            st.markdown("""
            <div style="
                background: rgba(255,255,255,0.90);
                backdrop-filter: blur(12px);
                color: #222;
                padding: 20px;
                border-radius: 15px;
                border: 2px solid #514a9d;
                font-size: 28px;
                font-weight: 900;
                text-align: center;
            ">
            🎥 Upload a video first, to generate summary.
            </div>
            """, unsafe_allow_html=True)
        
# =========================================================
# RIGHT
# =========================================================
# =========================================================
# RIGHT PANEL (CHAT)
# =========================================================
with right_col:

    st.markdown("## 💬 CineChat")

    if st.session_state.video_loaded:

        st.info("Ask anything about the uploaded video.")

        # Scrollable chat area
        chat_container = st.container(height=650)

        with chat_container:

            # Display previous conversation
            for sender, message in st.session_state.chat_history:

                if sender == "You":
                    st.markdown(
                        f"""
                        <div class="user-bubble">
                            <b>🧑 You</b><br><br>
                            {message}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                else:
                    st.markdown(
                        f"""
                        <div class="bot-bubble">
                            <b>🤖 CineChat</b><br><br>
                            {message}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

        # Chat input always stays at the bottom
        question = st.chat_input(
            "Ask a question about the uploaded video..."
        )

        if question:

            # Save user message
            st.session_state.chat_history.append(
                ("You", question)
            )

            # Generate answer
            with st.spinner("Thinking..."):
                answer = ask_question(question)

            # Save assistant response
            st.session_state.chat_history.append(
                ("CineChat", answer)
            )

            # Refresh page so the latest conversation appears
            st.rerun()

    else:

        st.markdown("""
        <div style="
            background: rgba(255,255,255,0.90);
            backdrop-filter: blur(12px);
            color: #222;
            padding: 20px;
            border-radius: 15px;
            border: 2px solid #514a9d;
            font-size: 28px;
            font-weight: 900;
            text-align: center;
        ">
        🎥 Upload a video first, then you can start chatting.
        </div>
        """, unsafe_allow_html=True)


st.markdown("</div>", unsafe_allow_html=True)