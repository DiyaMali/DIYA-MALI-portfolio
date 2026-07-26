import re
import os
import urllib.request
from PIL import Image

h_file = r'd:\diya portfolio\projects_page.html'
if not os.path.exists(h_file):
    print("projects_page.html not found!")
    exit()

with open(h_file, 'r', encoding='utf-8') as f:
    text = f.read()

# Extract all 28-35 char Google Drive IDs
candidate_ids = list(set(re.findall(r'1[a-zA-Z0-9_-]{28,34}', text)))
print(f"Found {len(candidate_ids)} candidate IDs in projects_page.html")

out_dir = r'd:\diya portfolio\assets\projects_hd'
os.makedirs(out_dir, exist_ok=True)

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
hd_count = 0

for fid in candidate_ids:
    # URL for maximum 4K HD resolution render
    url = f"https://lh3.googleusercontent.com/d/{fid}=s3840"
    try:
        req = urllib.request.Request(url, headers=headers)
        res = urllib.request.urlopen(req)
        data = res.read()
        if len(data) > 50000 and (b'PNG' in data[:20] or b'JFIF' in data[:20] or b'Exif' in data[:20] or b'WEBP' in data[:20]):
            hd_count += 1
            out_path = os.path.join(out_dir, f"proj_hd_{hd_count}.png")
            with open(out_path, 'wb') as out_f:
                out_f.write(data)
            img = Image.open(out_path)
            print(f" ==> SAVED FULL HD [{hd_count}]: {out_path} | Size={img.size} ({len(data)} bytes)")
    except Exception as e:
        pass

print(f"\nDone! Downloaded {hd_count} Full HD project images.")
