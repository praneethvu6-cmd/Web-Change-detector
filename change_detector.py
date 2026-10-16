import time
import requests
import hashlib
import difflib
from bs4 import BeautifulSoup
from selenium import webdriver

def capture_screenshot(url, filename):
    """Captures a background visual snapshot of the page using a headless browser."""
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  
        
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        time.sleep(2)
        
        driver.save_screenshot(filename)
        driver.quit()
        print(f"[LOG] Screenshot saved as '{filename}'")
    except Exception as e:
        print(f"[WARNING] Visual capture skipped: {e}")

def fetch_website_text(url):

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()  
        
        soup = BeautifulSoup(response.text, 'html.parser')
        raw_text = soup.get_text()
        
        
        return [line.strip() for line in raw_text.splitlines() if line.strip()]
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Connection check failed: {e}")
        return None

# --- Main CONTROLLER ---(for my sake to debug)
if __name__ == "__main__":
    target_url = input("🔗 Enter URL to monitor: ").strip()
    
    print("\n[SYSTEM] Initializing tracking baseline...")
    baseline_lines = fetch_website_text(target_url)
    
    if baseline_lines:

        baseline_string = "\n".join(baseline_lines)
        baseline_hash = hashlib.sha256(baseline_string.encode('utf-8')).hexdigest()
        print(f"[SYSTEM] Baseline locked. Signature: {baseline_hash[:10]}...")
        
        capture_screenshot(target_url, "baseline_snapshot.png")
        print("[SYSTEM] Background tracking loop active.\n")
        
        while True:
            try:
                time.sleep(10)  
                current_lines = fetch_website_text(target_url)
                
                if current_lines is None:
                    continue  
                current_string = "\n".join(current_lines)
                current_hash = hashlib.sha256(current_string.encode('utf-8')).hexdigest()
                
                print(f"[CHECK] Hash verified at {time.strftime('%X')}. Content matches baseline.")

                
                
                if current_hash != baseline_hash:
                    print(f"\n ALERT: Modification detected at {time.strftime('%X')}!")
                    print("--- Displaying Structural Differences ---")
                    
                    diff = difflib.ndiff(baseline_lines, current_lines)
                    for change in diff:
                        if change.startswith('+ ') or change.startswith('- '):
                            print(change)
                    print("----------------------------------------\n")
                    
                    capture_screenshot(target_url, "modified_snapshot.png")
                    baseline_lines = current_lines
                    baseline_hash = current_hash
                    
            except KeyboardInterrupt:
                print("\n[SYSTEM] Monitoring engine halted safely. Exiting.")
                break
    else:
        print("Could not connect to target URL.")
