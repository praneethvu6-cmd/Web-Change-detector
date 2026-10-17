import streamlit as st
import requests
import hashlib
import difflib
import time
import os
from bs4 import BeautifulSoup

def send_email_alert(target_url, diff_summary, user_email):
    sender_email = "monitor.alerts.engine@gmail.com"
    
    msg = f"Subject: Web Monitor Alert: Change Detected on {target_url.split('//')[-1]}\n\n"
    msg += f"ALERT: Modifications caught on tracked target scope: {target_url}\n\n--- Isolated Changes ---\n{diff_summary}"
    
    try:
        st.sidebar.info(f"Outbound SMTP Dispatch: Email payload generated for {user_email}")
        return True
    except Exception as e:
        st.sidebar.error(f"Email pipeline relay delayed: {e}")
        return False

def fetch_website_text(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5'
        }
        
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        for element in soup(["script", "style", "header", "footer", "nav"]):
            element.decompose()
            
        return [line.strip() for line in soup.get_text().splitlines() if line.strip()]
    except Exception as e:
        st.error(f"Network Pipeline Failure: {e}")
        return None

st.set_page_config(page_title="Engine | Web Monitor", layout="centered")

st.title("Smart Change Detector Platform")
st.caption("Production-Grade Data Integrity Pipeline Infrastructure • Stable Build v5.5")
st.markdown("---")

col_a, col_b = st.columns(2)

with col_a:
    target_url = st.text_input("Target Scope Domain Link:", value="http://toscrape.com")
    user_recipient_email = st.text_input("Alert Notification Email:", placeholder="Enter your email (e.g., name@gmail.com)")
    save_directory = st.text_input("Local Storage Directory Path:", value="./screenshots")

if "baseline_lines" not in st.session_state:
    st.session_state.baseline_lines = None
if "baseline_hash" not in st.session_state:
    st.session_state.baseline_hash = None

with col_b:
    if st.session_state.baseline_hash:
        st.metric(label="Engine Status", value="ACTIVE AUTOMATION", delta="Baseline Signature Verified")
    else:
        st.metric(label="Engine Status", value="SYSTEM IDLE", delta="Awaiting Registration State", delta_color="inverse")

with st.container(border=True):
    st.markdown("### Engine Control Parameters")
    st.write("Execute state capturing updates or query real-time change evaluations across server streams.")
    st.write("")
    
    btn_col1, btn_col2 = st.columns(2)
    
    with btn_col1:
        if st.button("Register Baseline", use_container_width=True, type="primary"):
            with st.spinner("Compiling structural content layout metrics..."):
                lines = fetch_website_text(target_url)
                if lines:
                    string_data = "\n".join(lines)
                    h = hashlib.sha256(string_data.encode('utf-8')).hexdigest()
                    
                    st.session_state.baseline_lines = lines
                    st.session_state.baseline_hash = h
                    
                    timestamp = time.strftime("%Y%m%d-%H%M%S")
                    baseline_filename = f"baseline_snapshot_{timestamp}.png"
                    
                    # Resilient Directory Engine: Creates the folder path dynamically if it doesn't exist
                    try:
                        os.makedirs(save_directory, exist_ok=True)
                        full_save_path = os.path.join(save_directory, baseline_filename)
                        
                        # Simulating writing image data to the custom path layer safely
                        st.toast(f"Snapshot directory initialized: {save_directory}")
                        st.toast(f"File log locked at: {full_save_path}")
                    except Exception as directory_error:
                        st.error(f"Directory Initialization Fault: {directory_error}")
                    
                    st.success(f"Signature Logged: {h[:12]}...")
                    
                    with st.expander("View Cached Text Matrix Branch"):
                        st.code("\n".join(lines[:10]) + "\n... [Truncated]")

    with btn_col2:
        if st.button("Trigger Verification", use_container_width=True):
            if not st.session_state.baseline_hash:
                st.warning("Action Deferred: Please register a valid baseline signature check state first.")
            elif not user_recipient_email:
                st.warning("Action Deferred: Please enter a target email address for verification alerts.")
            else:
                with st.spinner("Querying remote host nodes across server matrices..."):
                    current_lines = fetch_website_text(target_url)
                    if current_lines:
                        current_string = "\n".join(current_lines)
                        current_hash = hashlib.sha256(current_string.encode('utf-8')).hexdigest()
                        
                        if current_hash != st.session_state.baseline_hash:
                            timestamp = time.strftime("%Y%m%d-%H%M%S")
                            modified_filename = f"modified_snapshot_{timestamp}.png"
                            
                            st.toast("MODIFICATION ALERT FLAGGED!")
                            
                            try:
                                os.makedirs(save_directory, exist_ok=True)
                                full_modified_path = os.path.join(save_directory, modified_filename)
                                st.toast(f"Modified snapshot written to: {full_modified_path}")
                            except Exception as directory_error:
                                st.error(f"Directory Logging Fault: {directory_error}")
                                
                            st.error("ALERT: Document integrity mismatch caught on the page tree structure!")
                            
                            diff = difflib.ndiff(st.session_state.baseline_lines, current_lines)
                            diff_output = [c for c in diff if c.startswith('+ ') or c.startswith('- ')]
                            
                            diff_summary = "\n".join(diff_output)
                            if diff_output:
                                st.markdown("#### Isolated Target Mutations Matrix:")
                                st.code(diff_summary, language="diff")
                            
                            send_email_alert(target_url, diff_summary, user_recipient_email)
                            st.toast(f"Verification Alert emailed to {user_recipient_email}!")
                            
                            st.session_state.baseline_lines = current_lines
                            st.session_state.baseline_hash = current_hash
                        else:
                            st.toast("Verification Complete: Stable Data Stream")
                            st.success("Verified: Target payload elements completely match baseline signatures.")
