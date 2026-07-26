import urllib.request
import re
import json
import os

url = "https://drive.google.com/drive/folders/1AGu61KNI10AM-9g30R2wi6rHBB4gUE7_?usp=sharing"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
html = urllib.request.urlopen(req).read().decode('utf-8')

# Find all 28-33 alphanumeric string candidates
ids = set(re.findall(r'1[a-zA-Z0-9_-]{32}', html))
print(f"Found {len(ids)} ID candidates in main folder")

# Download each candidate folder to see which one contains 'projects'
for fid in ids:
    try:
        f_url = f"https://drive.google.com/drive/folders/{fid}"
        f_req = urllib.request.Request(f_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        f_html = urllib.request.urlopen(f_req).read().decode('utf-8')
        if "projects" in f_html.lower() or "sprout" in f_html.lower() or "chunav" in f_html.lower() or "viralsim" in f_html.lower():
            print(f"MATCH FOUND for folder/file ID: {fid}")
            # find all file IDs inside
            img_ids = set(re.findall(r'1[a-zA-Z0-9_-]{32}', f_html))
            print(f"  Found {len(img_ids)} sub-IDs in this folder")
    except Exception as e:
        pass
