import streamlit as st
import requests
import hashlib
import difflib
import time
from bs4 import BeautifulSoup

def fetch_website_text(url):
    """Safely handles outbound network pipeline requests and sanitizes raw data parsing layers."""
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Clean non-content elements to optimize text matching
        for element in soup(["script", "style", "header", "footer", "nav"]):
            element.decompose()
            
        return [line.strip() for line in soup.get_text().splitlines() if line.strip()]
    except Exception as e:
        st.error(f"❌ Network Pipeline Interrupt: {e}")
        return None

# --- ADVANCED WINDOW PORTAL CONFIGURATIONS ---
st.set_page_config(
    page_title="Engine | Web Monitor", 
    page_icon="🔍", 
    layout="centered"
)

# Custom Clean Main Header Layout
st.title("🔍 Smart Change Detector Platform")
st.caption("Production-Grade Data Integrity Pipeline Infrastructure • Stable Build v2.5")
st.markdown("---")

# Layout Column Structure for Input vs Status Tracking Metrics
col_a, col_b = st.columns(2)

with col_a:
    target_url = st.text_input("🎯 Target Scope Domain Link:", value="http://toscrape.com")

# Persistent Client Session Memory Allocations
if "baseline_lines" not in st.session_state:
    st.session_state.baseline_lines = None
if "baseline_hash" not in st.session_state:
    st.session_state.baseline_hash = None

with col_b:
    # Dynamic System Status Monitoring Metric Display Rules
    if st.session_state.baseline_hash:
        st.metric(label="Engine Status", value="ACTIVE AUTOMATION", delta="Baseline Signature Verified")
    else:
        st.metric(label="Engine Status", value="SYSTEM IDLE", delta="- Awaiting Registration State", delta_color="inverse")

# Central Controller Bounding Panel Card View Block
with st.container(border=True):
    st.markdown("### ⚙️ Engine Control Parameters")
    st.write("Execute state capturing updates or query real-time change evaluations across server streams.")
    st.write("")
    
    # Dual Execution Control Actions Column Rules
    btn_col1, btn_col2 = st.columns(2)
    
    with btn_col1:
        if st.button("🔒 Step 1: Register Baseline", use_container_width=True, type="primary"):
            with st.spinner("Compiling structural content layout metrics..."):
                lines = fetch_website_text(target_url)
                if lines:
                    string_data = "\n".join(lines)
                    h = hashlib.sha256(string_data.encode('utf-8')).hexdigest()
                    
                    st.session_state.baseline_lines = lines
                    st.session_state.baseline_hash = h
                    st.toast("🎯 Baseline Data Snapshot Saved Completely!")
                    st.success(f"Signature Logged: {h[:12]}...")
                    
                    # Display a quick collapsible sample view of what text was locked in
                    with st.expander("📄 View Cached Text Matrix Branch"):
                        st.code("\n".join(lines[:10]) + "\n... [Truncated for readability]")

    with btn_col2:
        if st.button("🔄 Step 2: Trigger Verification", use_container_width=True):
            if not st.session_state.baseline_hash:
                st.warning("Action Deferred: Please register a valid baseline signature check state first.")
            else:
                with st.spinner("Querying remote host nodes across server matrices..."):
                    current_lines = fetch_website_text(target_url)
                    if current_lines:
                        current_string = "\n".join(current_lines)
                        current_hash = hashlib.sha256(current_string.encode('utf-8')).hexdigest()
                        
                        if current_hash != st.session_state.baseline_hash:
                            st.toast("⚠️ MODIFICATION ALERT FLAGGED!", icon="🚨")
                            st.error("🚨 ALERT: Document integrity mismatch caught on the page tree structure!")
                            
                            # Execute line-by-line structural diff sequence evaluation maps
                            diff = difflib.ndiff(st.session_state.baseline_lines, current_lines)
                            diff_output = [c for c in diff if c.startswith('+ ') or c.startswith('- ')]
                            
                            if diff_output:
                                st.markdown("#### 🛠️ Isolated Target Mutations Matrix:")
                                st.code("\n".join(diff_output), language="diff")
                            
                            # Synchronize cache layers to mirror newly verified baseline updates
                            st.session_state.baseline_lines = current_lines
                            st.session_state.baseline_hash = current_hash
                        else:
                            st.toast("✅ Verification Complete: Stable Data Stream", icon="🛡️")
                            st.success("✅ Verified: Target payload elements completely match baseline signatures.")
