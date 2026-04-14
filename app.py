import streamlit as st, subprocess, uuid, os, shutil, time, zipfile, io, requests
from pathlib import Path as P
from PIL import Image, ImageDraw, ImageFont
import numpy as np

st.set_page_config(page_title="MP3 to MP4 - @qozma", layout="centered", page_icon="🎵")

if "conversions" not in st.session_state:
    st.session_state.conversions = []

def log(msg):
    if "debug_log" not in st.session_state:
        st.session_state.debug_log = []
    st.session_state.debug_log.append(f"[{time.strftime('%H:%M:%S')}] {msg}")

def get_dims(fmt):
    return {"16:9": (1280, 720), "9:16": (720, 1280), "1:1": (720, 720)}.get(fmt, (1280, 720))

def download_bg(url, path):
    try:
        r = requests.get(url, timeout=30, headers={"User-Agent": "Mozilla/5.0"})
        r.raise_for_status()
        path.write_bytes(r.content)
        return True
    except:
        return False

def generate_music_bg(width, height, bg_type="16:9"):
    gradients = [((102, 126, 234), (118, 75, 162)), ((240, 147, 251), (245, 87, 108)), ((67, 233, 123), (56, 161, 105)), ((250, 112, 154), (254, 225, 64))]
    color1, color2 = gradients[uuid.uuid4().int % len(gradients)]
    img = Image.new("RGB", (width, height))
    pixels = img.load()
    for i in range(width):
        for j in range(height):
            ratio = i / width if bg_type == "9:16" else j / height
            r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
            g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
            b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
            pixels[i, j] = (r, g, b)
    return img

st.markdown("<div style='background: linear-gradient(135deg, #0066cc, #004999); padding: 2rem; border-radius: 12px; margin-bottom: 2rem; text-align: center; color: white;'><h1 style='margin: 0;'>🎵 MP3 to MP4 Converter</h1><p style='margin: 0.5rem 0 0 0;'>@qozma • Лого + Субтитры</p></div>", unsafe_allow_html=True)

uploaded = st.file_uploader("📁 Drop MP3 files", type=["mp3","wav","m4a","aac","flac","ogg"], accept_multiple_files=True)
if uploaded:
    st.success(f"✅ {len(uploaded)} file(s)")

if uploaded:
    col1, col2 = st.columns(2)
    with col1:
        fmt = st.selectbox("Format", ["16:9", "9:16", "1:1"])
    with col
@'
import streamlit as st, subprocess, uuid, os, shutil, time, zipfile, io, requests
from pathlib import Path as P
from PIL import Image, ImageDraw, ImageFont
import numpy as np

st.set_page_config(page_title="MP3 to MP4 - @qozma", layout="centered", page_icon="🎵")

if "conversions" not in st.session_state:
    st.session_state.conversions = []

def log(msg):
    if "debug_log" not in st.session_state:
        st.session_state.debug_log = []
    st.session_state.debug_log.append(f"[{time.strftime('%H:%M:%S')}] {msg}")

def get_dims(fmt):
    return {"16:9": (1280, 720), "9:16": (720, 1280), "1:1": (720, 720)}.get(fmt, (1280, 720))

def download_bg(url, path):
    try:
        r = requests.get(url, timeout=30, headers={"User-Agent": "Mozilla/5.0"})
        r.raise_for_status()
        path.write_bytes(r.content)
        return True
    except:
        return False

def generate_music_bg(width, height, bg_type="16:9"):
    gradients = [((102, 126, 234), (118, 75, 162)), ((240, 147, 251), (245, 87, 108)), ((67, 233, 123), (56, 161, 105)), ((250, 112, 154), (254, 225, 64))]
    color1, color2 = gradients[uuid.uuid4().int % len(gradients)]
    img = Image.new("RGB", (width, height))
    pixels = img.load()
    for i in range(width):
        for j in range(height):
            ratio = i / width if bg_type == "9:16" else j / height
            r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
            g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
            b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
            pixels[i, j] = (r, g, b)
    return img

st.markdown("<div style='background: linear-gradient(135deg, #0066cc, #004999); padding: 2rem; border-radius: 12px; margin-bottom: 2rem; text-align: center; color: white;'><h1 style='margin: 0;'>🎵 MP3 to MP4 Converter</h1><p style='margin: 0.5rem 0 0 0;'>@qozma • Лого + Субтитры</p></div>", unsafe_allow_html=True)

uploaded = st.file_uploader("📁 Drop MP3 files", type=["mp3","wav","m4a","aac","flac","ogg"], accept_multiple_files=True)
if uploaded:
    st.success(f"✅ {len(uploaded)} file(s)")

if uploaded:
    col1, col2 = st.columns(2)
    with col1:
        fmt = st.selectbox("Format", ["16:9", "9:16", "1:1"])
    with col2:
        bitrate = st.selectbox("Quality", ["320k", "192k", "128k"])
    
    logo_pos = st.selectbox("Logo Position", ["none", "bottom_right", "bottom_left", "top_right", "top_left"])
    logo_file = st.file_uploader("Upload logo (PNG)", type=["png"])
    
    subtitles = st.text_area("📝 Subtitles (poetry text):", placeholder="Вставьте текст стиха...")
    
    if st.button("🚀 CONVERT", type="primary", use_container_width=True):
        progress = st.progress(0)
        status = st.empty()
        w, h = get_dims(fmt)
        
        # Save logo
        logo_path = None
        if logo_file and logo_pos != "none":
            logo_path = P("uploads") / f"logo.png"
            P("uploads").mkdir(exist_ok=True)
            logo_path.write_bytes(logo_file.getvalue())
        
        for i, file in enumerate(uploaded):
            status.text(f"{i+1}/{len(uploaded)}: {file.name}")
            try:
                jid = str(uuid.uuid4())
                inp = P("uploads") / f"{jid}_in.mp3"
                out = P("uploads") / f"{jid}_out.mp4"
                bg = P("uploads") / f"{jid}_bg.png"
                P("uploads").mkdir(exist_ok=True)
                
                with open(inp, "wb") as f:
                    f.write(file.getvalue())
                
                generate_music_bg(w, h, fmt).save(bg)
                
                # Build FFmpeg command
                cmd = ["ffmpeg","-y","-loop","1","-i",str(bg),"-i",str(inp),"-c:v","libx264","-pix_fmt","yuv420p","-s",f"{w}x{h}","-c:a","aac","-b:a",bitrate,"-shortest"]
                
                if logo_path and subtitles:
                    # Logo + Subtitles
                    esc_text = subtitles.replace("'", "'\\''")
                    logo_filter = f"[1:v]scale=150:150[lg];[0:v][lg]overlay="
                    if logo_pos == "bottom_right":
                        logo_filter += "W-w-20:H-h-20"
                    elif logo_pos == "bottom_left":
                        logo_filter += "20:H-h-20"
                    elif logo_pos == "top_right":
                        logo_filter += "W-w-20:20"
                    else:
                        logo_filter += "20:20"
                    cmd += ["-filter_complex", f"{logo_filter},drawtext=text='{esc_text}':fontsize=36:fontcolor=white:x=(w-text_w)/2:y=h-text_h-50:shadowcolor=black:shadowx=2:shadowy=2","-map","0:v","-map","1:a",str(out)]
                elif logo_path:
                    # Logo only
                    logo_filter = f"[1:v]scale=150:150[lg];[0:v][lg]overlay="
                    if logo_pos == "bottom_right":
                        logo_filter += "W-w-20:H-h-20[v]"
                    elif logo_pos == "bottom_left":
                        logo_filter += "20:H-h-20[v]"
                    elif logo_pos == "top_right":
                        logo_filter += "W-w-20:20[v]"
                    else:
                        logo_filter += "20:20[v]"
                    cmd += ["-filter_complex", logo_filter, "-map", "[v]", "-map", "1:a", str(out)]
                elif subtitles:
                    # Subtitles only
                    esc_text = subtitles.replace("'", "'\\''")
                    cmd += ["-vf", f"drawtext=text='{esc_text}':fontsize=36:fontcolor=white:x=(w-text_w)/2:y=h-text_h-50:shadowcolor=black:shadowx=2:shadowy=2", str(out)]
                else:
                    # No filters
                    cmd += [str(out)]
                
                r = subprocess.run(cmd, capture_output=True, text=True)
                if r.returncode != 0:
                    raise Exception(r.stderr[-300:])
                
                with open(out, "rb") as f:
                    data = f.read()
                st.session_state.conversions.append({"name": file.name.rsplit(".",1)[0]+".mp4", "data": data, "size": len(data)})
                
                for p in [inp, out, bg]:
                    try: P(p).unlink()
                    except: pass
                    
            except Exception as e:
                st.error(f"❌ {file.name}: {e}")
            
            progress.progress((i+1)/len(uploaded))
        
        if logo_path:
            try: logo_path.unlink()
            except: pass
        
        st.success(f"✅ Done! Scroll down to download.")
    
    if st.session_state.conversions:
        st.markdown("### 📥 Download")
        for i, conv in enumerate(st.session_state.conversions):
            st.download_button(f"📥 {conv['name']}", data=conv["data"], file_name=conv["name"], mime="video/mp4", key=f"dl_{i}")
        if len(st.session_state.conversions) > 1:
            zip_buf = io.BytesIO()
            with zipfile.ZipFile(zip_buf, "w") as zf:
                for c in st.session_state.conversions:
                    zf.writestr(c["name"], c["data"])
            st.download_button("📦 Download ALL (ZIP)", data=zip_buf.getvalue(), file_name="all.zip", mime="application/zip", type="primary")

st.markdown("---")
st.caption("@qozma «Поэзия и музыка»")
