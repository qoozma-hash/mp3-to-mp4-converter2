import streamlit as st
import subprocess, os, tempfile
from pathlib import Path
from PIL import Image

st.set_page_config(page_title="MP3 to MP4 Converter - FreeConvert", layout="wide", page_icon="🎬")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');
    * { font-family: 'Roboto', sans-serif; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .main { background: #f8f9fa; padding: 0; max-width: 100%; }
    .header { background: white; border-bottom: 1px solid #e0e0e0; padding: 1rem 2rem; display: flex; align-items: center; justify-content: space-between; }
    .logo { font-size: 1.8rem; font-weight: 700; color: #6c5ce7; }
    .nav-links { display: flex; gap: 2rem; color: #333; font-size: 0.95rem; }
    .nav-links span { cursor: pointer; font-weight: 500; }
    .container { max-width: 1000px; margin: 0 auto; padding: 3rem 2rem; }
    .main-title { font-size: 3rem; font-weight: 700; text-align: center; color: #2d3748; margin: 1rem 0 0.5rem 0; }
    .subtitle { font-size: 1.3rem; text-align: center; color: #718096; margin-bottom: 3rem; }
    .upload-area { background: white; border: 2px dashed #cbd5e0; border-radius: 12px; padding: 3rem 2rem; text-align: center; margin: 2rem 0; }
    .add-files-btn { background: #6c5ce7; color: white; padding: 1rem 2rem; border-radius: 8px; font-size: 1.1rem; font-weight: 600; display: inline-block; margin: 1rem 0; cursor: pointer; }
    .file-item { background: white; border: 1px solid #e2e8f0; border-radius: 8px; padding: 1.5rem; margin: 1rem 0; display: flex; align-items: center; justify-content: space-between; }
    .file-info { flex: 1; text-align: left; }
    .file-name { font-size: 1.1rem; font-weight: 600; color: #2d3748; margin-bottom: 0.5rem; }
    .file-size { font-size: 0.9rem; color: #718096; }
    .output-select { display: flex; align-items: center; gap: 1rem; margin: 1rem 0; }
    .output-label { font-size: 1rem; color: #4a5568; font-weight: 500; }
    .format-badge { background: #6c5ce7; color: white; padding: 0.5rem 1rem; border-radius: 6px; font-weight: 600; }
    .convert-btn { background: #6c5ce7; color: white; padding: 1.2rem 3rem; border-radius: 8px; font-size: 1.2rem; font-weight: 700; border: none; cursor: pointer; width: 100%; margin: 1.5rem 0; display: flex; align-items: center; justify-content: center; gap: 0.5rem; }
    .convert-btn:hover { background: #5b4cdb; }
    .download-section { background: white; border: 2px solid #48bb78; border-radius: 12px; padding: 2rem; text-align: center; margin: 2rem 0; }
    .download-btn { background: #6c5ce7; color: white; padding: 1.5rem 4rem; border-radius: 8px; font-size: 1.3rem; font-weight: 700; border: none; cursor: pointer; margin: 1rem 0; }
    .sidebar { background: white; border: 1px solid #e2e8f0; border-radius: 8px; padding: 1.5rem; margin: 1rem 0; }
    .sidebar-title { font-size: 1rem; font-weight: 600; color: #2d3748; margin-bottom: 1rem; }
    .sidebar-link { display: block; padding: 0.75rem; color: #4a5568; text-decoration: none; border-radius: 6px; margin: 0.5rem 0; font-size: 0.95rem; }
    .sidebar-link:hover { background: #f7fafc; color: #6c5ce7; }
    .footer-info { background: white; border-top: 1px solid #e2e8f0; padding: 2rem; text-align: center; color: #718096; font-size: 0.9rem; margin-top: 3rem; }
    .stFileUploader {display: none;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="header">
    <div class="logo">🔄 FreeConvert</div>
    <div class="nav-links">
        <span>Convert</span>
        <span>Compress</span>
        <span>Tools</span>
        <span>API</span>
        <span>Pricing</span>
    </div>
    <div>
        <span style="margin-right: 1rem;">Log In</span>
        <span style="background: #6c5ce7; color: white; padding: 0.5rem 1rem; border-radius: 6px;">Sign Up</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="container">', unsafe_allow_html=True)

st.markdown('<h1 class="main-title">MP3 to MP4 Converter</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Convert MP3 to MP4 online, for free.</p>', unsafe_allow_html=True)

if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file = None
if 'converted' not in st.session_state:
    st.session_state.converted = False
if 'output_file' not in st.session_state:
    st.session_state.output_file = None

if not st.session_state.uploaded_file:
    st.markdown('<div class="upload-area">', unsafe_allow_html=True)
    st.markdown('<div class="add-files-btn">📁 Add More Files</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("", type=["mp3", "wav", "m4a", "ogg", "flac"], label_visibility="collapsed")
    if uploaded_file:
        st.session_state.uploaded_file = uploaded_file
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

if st.session_state.uploaded_file:
    file = st.session_state.uploaded_file
    file_size = file.size / (1024 * 1024)
    
    st.markdown(f"""
    <div class="file-item">
        <div class="file-info">
            <div class="file-name">🎵 {file.name}</div>
            <div class="file-size">{file_size:.2f} MB</div>
        </div>
        <div class="output-select">
            <span class="output-label">Output:</span>
            <span class="format-badge">MP4</span>
            <span style="cursor: pointer;">⚙️</span>
            <span style="cursor: pointer;">❌</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div style="background: #f7fafc; padding: 1rem; border-radius: 6px; margin: 1rem 0;">', unsafe_allow_html=True)
    st.markdown('<span style="color: #4a5568;">Added 1 files</span>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    if not st.session_state.converted:
        if st.button("▶️ Convert", key="convert_btn"):
            with st.spinner("Converting..."):
                with tempfile.TemporaryDirectory() as tmpdir:
                    audio_path = os.path.join(tmpdir, file.name)
                    with open(audio_path, "wb") as f:
                        f.write(file.getbuffer())
                    image_path = os.path.join(tmpdir, "image.jpg")
                    img = Image.new("RGB", (1920, 1080), color=(108, 92, 231))
                    img.save(image_path)
                    output_path = os.path.join(tmpdir, "output.mp4")
                    try:
                        cmd = ["ffmpeg", "-y", "-loop", "1", "-i", image_path, "-i", audio_path, "-c:v", "libx264", "-preset", "medium", "-b:v", "2500k", "-r", "30", "-c:a", "aac", "-b:a", "192k", "-vf", "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2", "-shortest", "-pix_fmt", "yuv420p", output_path]
                        subprocess.run(cmd, check=True, capture_output=True)
                        with open(output_path, "rb") as f:
                            st.session_state.output_file = f.read()
                        st.session_state.converted = True
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {str(e)[:200]}")
    
    if st.session_state.converted and st.session_state.output_file:
        st.markdown("""
        <div class="download-section">
            <h2 style="color: #48bb78; margin-bottom: 1rem;">✅ Conversion Complete!</h2>
            <p style="color: #718096; margin-bottom: 1.5rem;">Your file is ready for download</p>
        """, unsafe_allow_html=True)
        
        st.download_button("⬇️ Download MP4", st.session_state.output_file, file_name=Path(st.session_state.uploaded_file.name).stem + ".mp4", mime="video/mp4", key="download_btn")
        
        st.markdown("""
        <button class="convert-btn" style="margin-top: 1rem;">Convert More ➚</button>
        <p style="color: #718096; font-size: 0.9rem; margin-top: 1.5rem;">Converted files are automatically deleted after 8 hours to protect your privacy. Please download files before they are deleted.</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<div style="max-width: 1000px; margin: 0 auto; padding: 0 2rem;">
    <div class="sidebar">
        <div class="sidebar-title">Related Converters:</div>
        <a href="#" class="sidebar-link">▶️ Convert to MP4</a>
        <a href="#" class="sidebar-link">🎵 Free Convert to MP3</a>
        <a href="#" class="sidebar-link">🎬 Online Video Converter</a>
        <a href="#" class="sidebar-link">🎵 Convert Music to MP3</a>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="footer-info">
    <p>Converted files are automatically deleted after 8 hours to protect your privacy.</p>
    <p style="margin-top: 1rem;">© 2024 FreeConvert Clone • Free MP3 to MP4 Converter</p>
</div>
""", unsafe_allow_html=True)