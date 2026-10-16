# Web-Change-detector
A robust backend tracking engine built with Python that monitors webpages, alerts users to content changes, and saves visual logs.

this tracking system answers these questions

## Advanced Architectural Design Analysis

### 1. Is a site outage or CAPTCHA a change?
No. The application wraps the network pipeline inside a secure `try/except` guard block using `response.raise_for_status()`. If a target site crashes (500 Error), disappears (404 Error), or triggers an anti-bot CAPTCHA wall, the system safely catches the HTTP error exception, flags a system log, and skips straight to the next polling interval cycle without corrupting the baseline configuration states or sending false alerts.

### 2. If 200 users watch the same URL, is it fetched 200 times?
No. Hammering a target domain 200 separate times concurrently will trigger anti-scraping firewalls and block inbound connections. The architecture resolves this by implementing a centralized caching layer. The server performs exactly ONE single outbound request to the target site, converts the payload data string, and dynamically mirrors that single result stream from memory to all 200 users simultaneously.

### 3. How to avoid endless alerts on pages that differ on every load?
Websites update timestamps, view counters, and ad banners continuously. To prevent endless false change notifications, the engine routes raw page layers through `BeautifulSoup`. It actively invokes the `.decompose()` structural element method to strip out dynamic tracking scripts (`<script>`, `<style>`, `<header>`, `<footer`, `<nav>`) and normalizes content text line-by-line using `.splitlines()` before executing signature checks.

### 4. How to avoid hammering a site with requests?
The script uses managed polling intervals with `time.sleep()`. By enforcing safe time-controlled throttling thresholds between requests, the application respects target server architectures and completely avoids malicious high-velocity network behaviors.

