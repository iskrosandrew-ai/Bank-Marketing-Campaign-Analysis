import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from utils.data_loader import load_data
from utils.ai_engine import (
    detect_language,
    transcribe_audio_bytes,
    is_query_ambiguous,
    process_ai_query
)

st.set_page_config(
    page_title="AI Marketing Intelligence Assistant | Voice & Chat",
    page_icon="🤖",
    layout="wide"
)

# Custom High-End Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    .chat-header {
        background: linear-gradient(135deg, #1E1B4B 0%, #312E81 50%, #065F46 100%);
        padding: 2rem;
        border-radius: 16px;
        color: white;
        margin-bottom: 1.5rem;
    }
    
    .assistant-badge {
        display: inline-block;
        padding: 0.25rem 0.8rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 700;
        background-color: rgba(52, 211, 153, 0.2);
        color: #34D399;
        border: 1px solid rgba(52, 211, 153, 0.4);
        margin-bottom: 0.6rem;
    }
    
    .prompt-chip {
        display: inline-block;
        padding: 0.4rem 0.85rem;
        margin: 0.25rem;
        border-radius: 20px;
        background-color: #1E293B;
        color: #E2E8F0;
        border: 1px solid #475569;
        font-size: 0.85rem;
        cursor: pointer;
    }
    
    .clarification-box {
        background: rgba(245, 158, 11, 0.1);
        border: 1px solid rgba(245, 158, 11, 0.4);
        border-radius: 12px;
        padding: 1.2rem;
        color: #FBBF24;
        margin-top: 0.5rem;
        margin-bottom: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

df = load_data()

# Header Banner
st.markdown("""
<div class="chat-header">
    <span class="assistant-badge">🎙️ MULTIMODAL VOICE & NLP AGENT</span>
    <h2 style="margin:0; font-size:2.2rem; font-weight:700;">AI Marketing Intelligence Assistant</h2>
    <p style="margin-top:0.4rem; color:#CBD5E1; font-size:1.05rem;">
        Ask questions in <b>Egyptian Arabic</b> or <b>English</b> via text or microphone. 
        The AI interprets your inquiry, asks clarifying follow-ups if underspecified, and renders interactive Plotly visual charts.
    </p>
</div>
""", unsafe_allow_html=True)

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "👋 **Welcome! I am your Bank Marketing Intelligence Assistant.**\n\n"
                "You can query me by typing below or speaking through your microphone in **Egyptian Arabic** or **English**.\n\n"
                "أهلاً بك! أنا مساعدك الذكي لتحليل بيانات الحملة التسويقية. يمكنك التحدث معي باللهجة المصرية أو بالإنجليزية، وسأقوم بتحليل البيانات وعرض الرسوم البيانية التفاعلية فوراً."
            ),
            "fig": None
        }
    ]

# ----------------------------------------------------
# VOICE INPUT SECTION (NATIVE MICROPHONE)
# ----------------------------------------------------
with st.expander("🎙️ Voice Input via Microphone (تحدث عبر الميكروفون)", expanded=False):
    st.markdown("Record your voice question in Egyptian Arabic or English:")
    voice_lang = st.radio(
        "Spoken Language (لغة التسجيل):",
        options=["ar-EG (العامية المصرية)", "en-US (English)"],
        horizontal=True
    )
    selected_lang_code = "ar-EG" if "ar-EG" in voice_lang else "en-US"
    
    audio_val = st.audio_input("Press record and speak your query:")
    
    if audio_val is not None:
        with st.spinner("Processing speech audio..."):
            audio_bytes = audio_val.read()
            transcribed_text = transcribe_audio_bytes(audio_bytes, selected_lang_code)
            
            if transcribed_text and not transcribed_text.startswith("[Audio"):
                st.success(f"🗣️ Transcribed Query: **{transcribed_text}**")
                if st.button("🚀 Submit Transcribed Question"):
                    st.session_state["submitted_voice_query"] = transcribed_text
            else:
                st.warning("Could not decipher audio clearly. Please try speaking closer to the microphone or type below.")

# ----------------------------------------------------
# SUGGESTED PROMPT CHIPS
# ----------------------------------------------------
st.markdown("##### 💡 Suggested Questions / أسئلة مقترحة:")
chip_cols = st.columns(4)

prompts = [
    ("🇪🇬 ايه أكتر وظيفة بتشترك في الودائع؟", "ايه أكتر وظيفة بتشترك في الودائع؟"),
    ("🇪🇬 تأثير مدة المكالمة على الإقناع", "تأثير مدة المكالمة على الإقناع"),
    ("🇬🇧 Impact of housing loan on subscription", "Impact of housing loan on subscription"),
    ("🇬🇧 Marketing fatigue and contact frequency", "Marketing fatigue and contact frequency")
]

selected_chip = None
for i, (label, val) in enumerate(prompts):
    with chip_cols[i]:
        if st.button(label, key=f"chip_{i}", use_container_width=True):
            selected_chip = val

# Determine Active Query
active_query = None
if "submitted_voice_query" in st.session_state and st.session_state["submitted_voice_query"]:
    active_query = st.session_state["submitted_voice_query"]
    del st.session_state["submitted_voice_query"]
elif selected_chip:
    active_query = selected_chip

# Chat input widget
typed_query = st.chat_input("Ask a question in English or Egyptian Arabic (اسأل بالعربي أو الإنجليزي)...")
if typed_query:
    active_query = typed_query

# ----------------------------------------------------
# PROCESS QUERY
# ----------------------------------------------------
if active_query:
    # Append user question
    st.session_state.messages.append({"role": "user", "content": active_query, "fig": None})
    
    # 1. Check for Ambiguity / Clarifying Follow-ups
    is_ambiguous, clarify_msg, followups = is_query_ambiguous(active_query)
    
    if is_ambiguous:
        followup_text = clarify_msg
        if followups:
            followup_text += "\n\n**Suggested Options / مقترحات للتوضيح:**\n"
            for opt in followups:
                followup_text += f"- *{opt}*\n"
                
        st.session_state.messages.append({
            "role": "assistant",
            "content": followup_text,
            "fig": None
        })
    else:
        # 2. Process Clear Inquiry
        res = process_ai_query(active_query, df)
        st.session_state.messages.append({
            "role": "assistant",
            "content": res['text'],
            "fig": res.get('fig')
        })

# ----------------------------------------------------
# RENDER CHAT HISTORY
# ----------------------------------------------------
for idx, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("fig") is not None:
            st.plotly_chart(msg["fig"], use_container_width=True, key=f"chat_fig_{idx}")

# Clear Conversation Button
if len(st.session_state.messages) > 1:
    if st.button("🗑️ Clear Conversation History"):
        st.session_state.messages = [st.session_state.messages[0]]
        st.rerun()
