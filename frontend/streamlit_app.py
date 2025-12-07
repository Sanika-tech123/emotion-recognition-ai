import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from st_audiorec import st_audiorec

# Configuration
API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="Emotion AI - Professional Analytics",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Premium Professional CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Main Background with Gradient */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #4facfe 100%);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
        color: #ffffff;
        font-family: 'Inter', sans-serif;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Glassmorphism Container */
    .main .block-container {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(20px);
        border-radius: 24px;
        border: 1px solid rgba(255, 255, 255, 0.18);
        padding: 2.5rem;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    }
    
    /* Headers with Gradient Text */
    h1 {
        background: linear-gradient(135deg, #fff 0%, #e0e7ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important;
        font-size: 3rem !important;
        letter-spacing: -0.02em;
        margin-bottom: 0.5rem !important;
    }
    
    h2, h3 {
        color: #ffffff !important;
        font-weight: 600 !important;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    /* Text Area Styling */
    .stTextArea textarea {
        background: rgba(255, 255, 255, 0.95) !important;
        border: 2px solid rgba(139, 92, 246, 0.3) !important;
        color: #1f2937 !important;
        border-radius: 16px;
        font-size: 1rem;
        padding: 1rem;
        transition: all 0.3s ease;
    }
    .stTextArea textarea:focus {
        border-color: #8b5cf6 !important;
        box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.1) !important;
        transform: scale(1.01);
    }

    /* Premium Buttons */
    .stButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        border-radius: 12px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(102, 126, 234, 0.5);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    .stButton button:active {
        transform: translateY(0);
    }

    /* Metrics with Glass Effect */
    div[data-testid="stMetricValue"] {
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        background: linear-gradient(135deg, #fff 0%, #e0e7ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    div[data-testid="stMetricLabel"] {
        color: rgba(255, 255, 255, 0.9) !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        background: rgba(255, 255, 255, 0.1);
        padding: 8px;
        border-radius: 16px;
        backdrop-filter: blur(10px);
    }
    .stTabs [data-baseweb="tab"] {
        height: 56px;
        background: transparent;
        border-radius: 12px;
        color: rgba(255, 255, 255, 0.7);
        font-weight: 600;
        font-size: 1rem;
        border: none;
        transition: all 0.3s ease;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(255, 255, 255, 0.1);
        color: #ffffff;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.8), rgba(118, 75, 162, 0.8));
        color: #ffffff;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    
    /* File Uploader */
    [data-testid='stFileUploader'] {
        width: 100%;
    }
    [data-testid='stFileUploader'] section {
        padding: 1.5rem;
        background: rgba(255, 255, 255, 0.95);
        border: 2px dashed rgba(139, 92, 246, 0.4);
        border-radius: 16px;
        transition: all 0.3s ease;
    }
    [data-testid='stFileUploader'] section:hover {
        border-color: #8b5cf6;
        background: rgba(255, 255, 255, 1);
    }
    [data-testid='stFileUploader'] section > div {
        color: #4b5563 !important;
        font-weight: 500;
    }
    [data-testid='stFileUploader'] button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        margin-top: 12px;
        padding: 0.5rem 1.5rem;
        border-radius: 8px;
        font-weight: 600;
    }
    [data-testid='stFileUploader'] small {
        display: none;
    }
    
    /* Info boxes */
    .stAlert {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 12px;
        color: white;
    }
    
    /* Progress bars */
    .stProgress > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    /* Divider */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent 0%, rgba(255,255,255,0.3) 50%, transparent 100%);
        margin: 2rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Header ---
st.markdown("""
    <div style='text-align: center; margin-bottom: 2rem;'>
        <h1>🎭 Emotion AI Analytics</h1>
        <p style='font-size: 1.2rem; color: rgba(255,255,255,0.9); font-weight: 300;'>
            Advanced Multimodal Emotion Recognition Platform
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# --- Helper Functions ---
def plot_radar_chart(scores, title="Emotion Profile"):
    df = pd.DataFrame(dict(
        r=list(scores.values()),
        theta=list(scores.keys())
    ))
    fig = px.line_polar(df, r='r', theta='theta', line_close=True)
    fig.update_traces(
        fill='toself', 
        line_color='#fff', 
        fillcolor='rgba(255, 255, 255, 0.3)',
        line_width=3
    )
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True, 
                range=[0, 1], 
                showticklabels=False, 
                gridcolor='rgba(255,255,255,0.2)'
            ),
            angularaxis=dict(
                tickfont=dict(color='white', size=13, family='Inter'),
                gridcolor='rgba(255,255,255,0.2)'
            ),
            bgcolor='rgba(0,0,0,0)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        margin=dict(l=60, r=60, t=80, b=40),
        title=dict(
            text=title, 
            font=dict(color='white', size=18, family='Inter', weight=600),
            x=0.5,
            xanchor='center'
        ),
        font=dict(family='Inter')
    )
    return fig

def get_emoji(emotion):
    emotion = emotion.lower()
    emoji_map = {
        "happiness": "😄", "happy": "😄", "joy": "😄",
        "sadness": "😢", "sad": "😢",
        "anger": "😡", "angry": "😡",
        "fear": "😨", "fearful": "😨",
        "surprise": "😲", "surprised": "😲",
        "disgust": "😖",
        "neutral": "😐",
        "love": "❤️", "affection": "❤️",
        "confusion": "😕",
        "stress": "😰", "anxiety": "😰"
    }
    for key, emoji in emoji_map.items():
        if key in emotion:
            return emoji
    return "🤖"

# --- Main Content ---
tab1, tab2 = st.tabs(["✍️ Text Analysis", "🎙️ Voice Analysis"])

# --- Text Tab ---
with tab1:
    st.markdown("### 📝 Analyze Emotional Tone in Text")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        text_input = st.text_area(
            "Enter your text", 
            height=180, 
            placeholder="Type something... e.g., 'I am absolutely thrilled about this amazing opportunity!'",
            label_visibility="collapsed"
        )
        
        analyze_text = st.button("🔍 Analyze Emotion", key="analyze_text_btn", use_container_width=True)

    with col2:
        st.markdown("""
            <div style='padding: 1.5rem; background: rgba(255,255,255,0.1); border-radius: 12px; backdrop-filter: blur(10px);'>
                <h4 style='color: white; margin-top: 0;'>💡 Tips</h4>
                <ul style='color: rgba(255,255,255,0.9); font-size: 0.9rem; line-height: 1.8;'>
                    <li>Be expressive and clear</li>
                    <li>Use natural language</li>
                    <li>Try different emotions</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

    if analyze_text and text_input:
        with st.spinner("🧠 Analyzing..."):
            try:
                response = requests.post(f"{API_URL}/predict/text", json={"text": text_input})
                if response.status_code == 200:
                    data = response.json()["data"]
                    label = data["label"]
                    score = data["score"]
                    all_scores = data["all_scores"]
                    
                    st.markdown("---")
                    
                    res_col1, res_col2 = st.columns([1, 1])
                    
                    with res_col1:
                        st.markdown(f"""
                            <div style='text-align: center; padding: 2rem; background: rgba(255,255,255,0.1); 
                                        border-radius: 16px; backdrop-filter: blur(10px);'>
                                <div style='font-size: 4rem; margin-bottom: 1rem;'>{get_emoji(label)}</div>
                                <h2 style='margin: 0; font-size: 2rem;'>{label}</h2>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        st.markdown("<br>", unsafe_allow_html=True)
                        st.metric("Confidence Score", f"{score*100:.1f}%")
                        st.progress(score)
                        
                        st.markdown("<br>", unsafe_allow_html=True)
                        sorted_scores = sorted(all_scores.items(), key=lambda x: x[1], reverse=True)[:3]
                        st.markdown("#### 🏆 Top Predictions")
                        for emo, conf in sorted_scores:
                            st.write(f"**{emo}** {get_emoji(emo)}: {conf*100:.1f}%")

                    with res_col2:
                        st.plotly_chart(plot_radar_chart(all_scores, "Emotion Spectrum"), use_container_width=True)
                else:
                    st.error(f"❌ Error: {response.text}")
            except Exception as e:
                st.error(f"⚠️ Connection Error: {e}")

# --- Audio Tab ---
with tab2:
    st.markdown("### 🎤 Analyze Emotions in Voice")
    
    upload_col, record_col = st.columns(2)
    
    with upload_col:
        st.info("📁 Upload Audio File")
        audio_file = st.file_uploader("Choose .wav file", type=["wav"], label_visibility="collapsed")

    with record_col:
        st.info("🎙️ Record Your Voice")
        wav_audio_data = st_audiorec()

    # Session state
    if 'audio_result' not in st.session_state:
        st.session_state.audio_result = None

    if audio_file:
        st.session_state.current_audio = "upload"
        st.audio(audio_file, format="audio/wav")
        
        if st.button("🌊 Analyze Uploaded Audio", key="btn_upload", use_container_width=True):
            with st.spinner("🎧 Processing audio..."):
                try:
                    files = {"file": (audio_file.name, audio_file, "audio/wav")}
                    response = requests.post(f"{API_URL}/predict/audio", files=files)
                    
                    if response.status_code == 200:
                        st.session_state.audio_result = response.json()["data"]
                    else:
                        st.error(f"❌ Error: {response.json().get('detail', 'Unknown error')}")
                except Exception as e:
                    st.error(f"⚠️ Connection Error: {e}")

    elif wav_audio_data is not None:
        st.session_state.current_audio = "record"
        st.audio(wav_audio_data, format="audio/wav")
        
        if st.button("🌊 Analyze Recorded Audio", key="btn_record", use_container_width=True):
            with st.spinner("🎧 Processing recording..."):
                try:
                    files = {"file": ("recording.wav", wav_audio_data, "audio/wav")}
                    response = requests.post(f"{API_URL}/predict/audio", files=files)
                    
                    if response.status_code == 200:
                        st.session_state.audio_result = response.json()["data"]
                    else:
                        st.error(f"❌ Error: {response.json().get('detail', 'Unknown error')}")
                except Exception as e:
                    st.error(f"⚠️ Connection Error: {e}")
    
    
    # Display Results
    if st.session_state.audio_result:
        data = st.session_state.audio_result
        emotion = data["emotion"]
        confidence = data["confidence"]
        probs = data.get("all_scores", {})
        
        # More aggressive neutral suppression
        if "Neutral" in probs and probs["Neutral"] < 0.95:
            # If neutral confidence is <95%, reduce it by 70% (was 50%)
            probs["Neutral"] = probs["Neutral"] * 0.3
            # Recalculate top emotion after suppression
            if probs:
                emotion = max(probs, key=probs.get)
                confidence = probs[emotion]
        
        st.markdown("---")
        res_col1, res_col2 = st.columns([1, 1])
        
        with res_col1:
            st.markdown(f"""
                <div style='text-align: center; padding: 2rem; background: rgba(255,255,255,0.1); 
                            border-radius: 16px; backdrop-filter: blur(10px);'>
                    <div style='font-size: 4rem; margin-bottom: 1rem;'>{get_emoji(emotion)}</div>
                    <h2 style='margin: 0; font-size: 2rem;'>{emotion}</h2>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.metric("Confidence Score", f"{confidence*100:.1f}%")
            st.progress(confidence)
            
        with res_col2:
            st.plotly_chart(plot_radar_chart(probs, "Voice Emotion Profile"), use_container_width=True)
            
        if st.button("🔄 Clear Results", key="clear_results"):
            st.session_state.audio_result = None
            st.rerun()

# --- Footer ---
st.markdown("---")
st.markdown("""
    <div style='text-align: center; padding: 2rem;'>
        <p style='color: rgba(255,255,255,0.7); font-size: 0.9rem; margin: 0;'>
            Powered by Advanced AI Models | RoBERTa & Wav2Vec2
        </p>
    </div>
    """, unsafe_allow_html=True)
