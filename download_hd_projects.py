import urllib.request
import re
import os
from PIL import Image

# We parsed the Drive folder html and retrieved the 9 file IDs from the projects subfolder:
# Let's inspect the main folder HTML again to get all file IDs directly
url = "https://drive.google.com/drive/folders/1AGu61KNI10AM-9g30R2wi6rHBB4gUE7_?usp=sharing"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
html = urllib.request.urlopen(req).read().decode('utf-8')

# Search forlh3.googleusercontent.com or file ID tokens
file_ids = list(set(re.findall(r'https://lh3\.googleusercontent\.com/d/([a-zA-Z0-9_-]+)', html)))
print(f"Found {len(file_ids)} googleusercontent IDs in page")

# If none found via string, search regex for 33-char drive IDs
if not file_ids:
    file_ids = list(set(re.findall(r'"([a-zA-Z0-9_-]{33})"', html)))

out_dir = r"d:\diya portfolio\assets\projects_hd"
os.makedirs(out_dir, exist_ok=True)

count = 0
for fid in file_ids:
    # Use max resolution parameter =s3840 or =w3840-h2160
    hd_url = f"https://lh3.googleusercontent.com/d/{fid}=s3840"
    out_file = os.path.join(out_dir, f"hd_proj_{count+1}.png")
    try:
        urllib.request.urlretrieve(hd_url, out_file)
        img = Image.open(out_file)
        if img.size[0] > 300 and img.size[1] > 200:
            count += 1
            print(f"[{count}] Saved HD image {out_file}: {img.size} ({os.path.getsize(out_file)} bytes)")
        else:
            os.remove(out_file)
    except Exception as e:
        if os.path.exists(out_file):
            os.remove(out_file)

print(f"Total HD images saved: {count}")
