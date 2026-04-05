import streamlit as st
import subprocess, os, tempfile, time
from pathlib import Path
from PIL import Image

st.set_page_config(page_title="MP3 to MP4 Converter", layout="wide", page_icon="🎬")

PRO_KEYS = {"PRO2026": {"name": "Early User", "daily_limit": 100}, "PREMIUM": {"name": "Premium", "daily_limit": 500}, "TEST": {"name": "Test", "daily_limit": 20}}
THEMES = {"🟢 Light": {"bg": "#e8f5e9", "text": "#1b5e20", "btn": "#4caf50"}, "🌙 Dark": {"bg": "#121212", "text": "#ffffff", "btn": "#bb86fc"}, "💙 Blue": {"bg": "#e3f2fd", "text": "#0d47a1", "btn": "#2196f3"}, "💜 Purple": {"bg": "#f3e5f5", "text": "#4a148c", "btn": "#9c27b0"}}

if "daily_count" not in st.session_state: st.session_state.daily_count = 0
if "last_reset" not in st.session_state: st.session_state.last_reset = time.time()
if "pro_info" not in st.session_state: st.session_state.pro_info = None
if "stats" not in st.session_state: st.session_state.stats = {"total": 0, "today": 0, "by_resolution": {}}
if "selected_theme" not in st.session_state: st.session_state.selected_theme = "🟢 Light"
if time.time() - st.session_state.last_reset > 86400: st.session_state.daily_count = 0; st.session_state.last_reset = time.time(); st.session_state.stats["today"] = 0
DAILY_LIMIT = st.session_state.pro_info["daily_limit"] if st.session_state.pro_info else 10
theme = THEMES[st.session_state.selected_theme]

st.markdown(f"""<style>.stApp{{background:{theme["bg"]};color:{theme["text"]}}}.stButton>button{{background:{theme["btn"]};color:white;font-weight:700;border-radius:10px}}.instruction{{font-size:1.2rem;font-weight:600;background:rgba(255,255,255,0.4);padding:1rem;border-radius:8px;border-left:4px solid {theme["btn"]}}}.success-box{{background:rgba(76,175,80,0.3);padding:1rem;border-radius:8px}}.stats-box{{background:rgba(255,255,255,0.5);padding:1rem;border-radius:8px;margin:0.5rem 0}}</style>""", unsafe_allow_html=True)

with st.sidebar:
    st.header("🎨 Theme")
    sel = st.selectbox("Choose:", list(THEMES.keys()), index=list(THEMES.keys()).index(st.session_state.selected_theme))
    if sel != st.session_state.selected_theme: st.session_state.selected_theme = sel; st.rerun()
    st.divider()
    st.header("🔑 Pro")
    if st.session_state.pro_info:
        st.success(f"✅ {st.session_state.pro_info['name']}")
        if st.button("Logout"): st.session_state.pro_info = None; st.rerun()
    else:
        key = st.text_input("Key:", type="password", placeholder="PRO2026")
        if st.button("Activate"):
            if key in PRO_KEYS: st.session_state.pro_info = PRO_KEYS[key]; st.success(f"✅ {PRO_KEYS[key]['name']}"); st.rerun()
            else: st.error("❌ Invalid")
    st.divider()
    st.header("📊 Stats")
    st.markdown(f'<div class="stats-box">📈 Total: <b>{st.session_state.stats["total"]}</b></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="stats-box">📅 Today: <b>{st.session_state.stats["today"]}</b></div>', unsafe_allow_html=True)

st.title("🎬 MP3 to MP4 Converter")
st.markdown('<div class="instruction">📌 INSTRUCTION: 1) Theme → 2) Audio → 3) Image → 4) Settings → 5) Convert → 6) Download</div>', unsafe_allow_html=True)

st.markdown('<div class="instruction">⚙️ STEP 1: Video Settings</div>', unsafe_allow_html=True)
c1,c2,c3 = st.columns(3)
with c1:
    res = st.selectbox("Resolution:", ["144p","240p","360p","480p","720p HD","1080p Full HD","1440p 2K","2160p 4K","16:9","9:16","1:1","4:3"], index=5)
    rm = {"144p":(256,144),"240p":(426,240),"360p":(640,360),"480p":(854,480),"720p HD":(1280,720),"1080p Full HD":(1920,1080),"1440p 2K":(2560,1440),"2160p 4K":(3840,2160),"16:9":(1920,1080),"9:16":(1080,1920),"1:1":(1080,1080),"4:3":(1024,768)}
    w,h = rm[res]
with c2:
    vc = st.selectbox("Codec:", ["H.264","H.265"], index=0)
    cm = {"H.264":"libx264","H.265":"libx265"}
    q = st.select_slider("Quality:", options=["Eco","Standard","High","Max"], value="High")
    bm = {"Eco":"800k","Standard":"2500k","High":"5000k","Max":"10000k"}
    fps = st.selectbox("FPS:", [24,30,60], index=1)
with c3:
    st.subheader("🔊 Audio")
    ac = st.selectbox("Codec:", ["AAC","MP3","OPUS"], index=0)
    ab = st.select_slider("Bitrate:", options=["96k","128k","192k","256k","320k"], value="192k")
    vol = st.slider("Volume:", 50,200,100)
    fi = st.checkbox("Fade In")
    fo = st.checkbox("Fade Out")

st.markdown(f'<div class="instruction">🎵 STEP 2: Upload Audio (limit: {DAILY_LIMIT}/day)</div>', unsafe_allow_html=True)
m1,m2 = st.columns([2,1])
with m1:
    audios = st.file_uploader("📁 Drop files", type=["mp3","wav","m4a","ogg","flac"], accept_multiple_files=True)
    if audios:
        rem = DAILY_LIMIT - st.session_state.daily_count
        if len(audios)>rem: st.warning(f"⚠️ Remaining: {rem}"); audios=audios[:rem]
        st.success(f"✅ Uploaded: {len(audios)}")
with m2:
    st.markdown('<div class="instruction">🖼️ STEP 3: Image</div>', unsafe_allow_html=True)
    mode = st.radio("Mode:", ["One for all","Each file"], index=0)
    if mode=="One for all": img = st.file_uploader("📤 Cover", type=["png","jpg","jpeg","webp"])
    else: imgs = st.file_uploader("📤 Covers", type=["png","jpg","jpeg","webp"], accept_multiple_files=True)

st.markdown('<div class="instruction">🎬 STEP 4: Convert</div>', unsafe_allow_html=True)
btn = st.button("🚀 CONVERT", type="primary", disabled=not(audios and ((mode=="One for all" and img) or (mode=="Each file" and imgs))))
if btn:
    if st.session_state.daily_count>=DAILY_LIMIT: st.error(f"❌ Limit: {DAILY_LIMIT}/day"); st.stop()
    pb = st.progress(0); tx = st.empty(); res = []
    for i,a in enumerate(audios):
        tx.text(f"⏳ {i+1}/{len(audios)}: {a.name}")
        with tempfile.TemporaryDirectory() as td:
            ap = os.path.join(td,"audio"+Path(a.name).suffix)
            if mode=="One for all":
                ip = os.path.join(td,"image.jpg")
                with open(ip,"wb") as f: f.write(img.getbuffer())
            else:
                ip = os.path.join(td,f"image_{i}.jpg")
                with open(ip,"wb") as f: f.write(imgs[i].getbuffer())
            op = os.path.join(td,"output.mp4")
            with open(ap,"wb") as f: f.write(a.getbuffer())
            vf = f"scale={w}:{h}:force_original_aspect_ratio=decrease,pad={w}:{h}:(ow-iw)/2:(oh-ih)/2"
            af = []
            if vol!=100: af.append(f"volume={vol/100}")
            if fi: af.append("afade=t=in:st=0:d=2")
            if fo: af.append("afade=t=out:st=0:d=2")
            afc = ",".join(af) if af else None
            cmd = ["ffmpeg","-y","-loop","1","-i",ip,"-i",ap,"-c:v",cm[vc],"-preset","medium","-b:v",bm[q],"-r",str(fps),"-c:a",ac.lower(),"-b:a",ab,"-ac","2"]
            if afc: cmd.extend(["-af",afc])
            cmd.extend(["-vf",vf,"-shortest","-pix_fmt","yuv420p",op])
            try:
                subprocess.run(cmd,check=True,capture_output=True)
                with open(op,"rb") as f: d = f.read()
                res.append({"name":Path(a.name).stem+".mp4","data":d,"size":len(d)})
                st.session_state.daily_count+=1; st.session_state.stats["total"]+=1; st.session_state.stats["today"]+=1
                if res not in st.session_state.stats["by_resolution"]: st.session_state.stats["by_resolution"][res]=0
                st.session_state.stats["by_resolution"][res]+=1
            except Exception as e: res.append({"name":Path(a.name).stem+".mp4","error":str(e)[:100]})
        pb.progress((i+1)/len(audios))
    tx.text("✅ Done!")
    st.divider()
    st.markdown('<div class="instruction">📥 STEP 5: Download</div>', unsafe_allow_html=True)
    for r in res:
        c1,c2 = st.columns([4,1])
        with c1:
            if "error" in r: st.error(f"❌ {r['name']}: {r['error']}")
            else: st.markdown(f'<div class="success-box">✅ {r["name"]} • {r["size"]/1024/1024:.2f} MB</div>', unsafe_allow_html=True)
        with c2:
            if "data" in r: st.download_button("⬇️",r["data"],file_name=r["name"],mime="video/mp4",key=r["name"])
    rem = DAILY_LIMIT - st.session_state.daily_count
    st.markdown(f'<div style="text-align:center;padding:1rem;background:rgba(255,233,128,0.5);border-radius:8px;font-weight:600;">📊 Remaining: <span style="color:#d32f2f;font-size:1.5rem">{rem}</span> of {DAILY_LIMIT}</div>', unsafe_allow_html=True)
st.markdown("---")
st.caption("🔒 Files processed locally • Not stored on server • © 2026 MP3 to MP4 Converter")
