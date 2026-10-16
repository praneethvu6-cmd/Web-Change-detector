import streamlit as st
import requests
import hashlib
import difflib
from bs4 import BeautifulSoup

def fetch_website_text(url):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        raw_text = soup.get_text()
        return [line.strip() for line in raw_text.splitlines() if line.strip()]
    except Exception as e:
        st.error(f"[ERROR] Fetch failed: {e}")
        return None

# --- WEB UI INTERFACE ---
st.set_page_config(page_title="Web Monitor Engine", page_icon="🔍")
st.title("🔍 Website Change Detector Engine")
st.write("Professional backend tracking pipeline deployed live.")

target_url = st.text_input("🔗 Target URL to monitor:", value="http://toscrape.com")

# Persistent browser memory states
if "baseline_lines" not in st.session_state:
    st.session_state.baseline_lines = None
if "baseline_hash" not in st.session_state:
    st.session_state.baseline_hash = None

col1, col2 = st.columns(2)

with col1:
    if st.button("⚙️ Lock Baseline"):
        lines = fetch_website_text(target_url)
        if lines:
            string_data = "\n".join(lines)
            h = hashlib.sha256(string_data.encode('utf-8')).hexdigest()
            st.session_state.baseline_lines = lines
            st.session_state.baseline_hash = h
            st.success(f"Baseline Locked! Hash: {h[:10]}...")

with col2:
    if st.button("🔄 Check for Changes"):
        if not st.session_state.baseline_hash:
            st.warning("Please lock a baseline first!")
        else:
            current_lines = fetch_website_text(target_url)
            if current_lines:
                current_string = "\n".join(current_lines)
                current_hash = hashlib.sha256(current_string.encode('utf-8')).hexdigest()
                
                if current_hash != st.session_state.baseline_hash:
                    st.error("🚨 ALERT: Modification detected on the webpage text structure!")
                    diff = difflib.ndiff(st.session_state.baseline_lines, current_lines)
                    diff_output = [c for c in diff if c.startswith('+ ') or c.startswith('- ')]
                    if diff_output:
                        st.text_area("Visualizing Code Changes:", value="\n".join(diff_output), height=200)
                    
                    st.session_state.baseline_lines = current_lines
                    st.session_state.baseline_hash = current_hash
                else:
                    st.success("✅ Verified: Content remains completely identical to baseline.")
