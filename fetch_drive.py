import urllib.request
import re
import os
import shutil

# Copy Diya's photo first
diya_photo_src = r'C:\Users\Admin\.gemini\antigravity-ide\brain\69b3a52d-6ba7-461a-9134-d53d3f367f3c\media__1785065732408.jpg'
diya_photo_dst = r'd:\diya portfolio\diya_portrait.jpg'
if os.path.exists(diya_photo_src):
    shutil.copyfile(diya_photo_src, diya_photo_dst)
    print("Copied Diya photo to diya_portrait.jpg")

url = 'https://drive.google.com/drive/folders/1AGu61KNI10AM-9g30R2wi6rHBB4gUE7_?usp=sharing'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
try:
    html = urllib.request.urlopen(req).read().decode('utf-8', errors='ignore')
    print('Drive page length:', len(html))
    
    # Save drive HTML for analysis
    with open('drive_page.html', 'w', encoding='utf-8') as f:
        f.write(html)
        
    # Search for image filenames and Google Drive file IDs
    # Common pattern in Google Drive folder HTML: ["FILE_ID", "FILENAME.ext"]
    file_ids = set(re.findall(r'1[a-zA-Z0-9_-]{32,34}', html))
    print(f'Found {len(file_ids)} candidate Drive File IDs:')
    for fid in file_ids:
        print(fid)
        
except Exception as e:
    print('Error:', e)
