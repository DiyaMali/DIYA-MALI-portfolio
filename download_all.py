import re
import os
import json
import urllib.request

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

def extract_and_download(folder_name, html_file):
    if not os.path.exists(html_file):
        return
    with open(html_file, 'r', encoding='utf-8') as f:
        text = f.read()
        
    out_dir = os.path.join('d:\\diya portfolio', folder_name)
    os.makedirs(out_dir, exist_ok=True)
    
    # Extract all string tokens that look like Google Drive IDs
    # Drive IDs are typically 28-35 alphanumeric chars with underscores or hyphens
    tokens = set(re.findall(r'[\"\']([1a-zA-Z0-9_-]{28,34})[\"\']', text))
    print(f"\n[{folder_name}] Found {len(tokens)} candidate ID tokens.")
    
    success_count = 0
    for idx, token in enumerate(tokens):
        # Skip folder IDs or known structural tokens
        if token in ['1AGu61KNI10AM-9g30R2wi6rHBB4gUE7_', '1T5SJXy1xc-34s1R76lhPW7amiBXrkfWm', '1a0njhsLBbBE2KLDbKaFm2gsZU9ORNzzj']:
            continue
            
        urls_to_try = [
            f"https://lh3.googleusercontent.com/d/{token}",
            f"https://drive.google.com/uc?export=download&id={token}",
            f"https://drive.google.com/thumbnail?id={token}&sz=w1000"
        ]
        
        for url in urls_to_try:
            try:
                req = urllib.request.Request(url, headers=headers)
                res = urllib.request.urlopen(req, timeout=5)
                data = res.read()
                # Check if valid image data (JPEG, PNG, WEBP)
                if len(data) > 3000 and (data[:4] == b'\xff\xd8\xff\xe0' or data[:4] == b'\xff\xd8\xff\xe1' or data[:4] == b'\x89PNG' or b'JFIF' in data[:20] or b'Exif' in data[:20] or b'VP8' in data[:30]):
                    ext = 'png' if b'PNG' in data[:10] else 'jpg'
                    filepath = os.path.join(out_dir, f"{folder_name}_img_{success_count+1}.{ext}")
                    with open(filepath, 'wb') as out_f:
                        out_f.write(data)
                    print(f"  [+] Downloaded: {filepath} ({len(data)} bytes) from ID {token}")
                    success_count += 1
                    break
            except Exception as e:
                pass

    print(f"[{folder_name}] Successfully downloaded {success_count} images.")

extract_and_download('experinces', 'experinces_page.html')
extract_and_download('projects', 'projects_page.html')
