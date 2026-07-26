import re
import urllib.request
import os

with open('drive_page.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Look for image names and file IDs in the JavaScript data payload
# Google Drive JSON payloads include array structures like: ["FILE_ID", "FILENAME.ext", ...]
matches = re.findall(r'\["([1a-zA-Z0-9_-]{28,36})",\s*"([^"]+\.(?:jpg|jpeg|png|webp|gif|JPG|PNG))"', content)
print("Found direct filename matches:", len(matches))
for fid, fname in matches:
    print(f"ID: {fid} | Name: {fname}")

# Fallback: find candidate file IDs and download test
candidates = set(re.findall(r'1[a-zA-Z0-9_-]{28,34}', content))
folder_id = '1AGu61KNI10AM-9g30R2wi6rHBB4gUE7_'

valid_ids = [c for c in candidates if c != folder_id and len(c) >= 28 and '-' not in c[-3:]]

print(f"\nTesting {len(valid_ids)} candidate IDs...")
os.makedirs('experience_images', exist_ok=True)

downloaded = []
for idx, fid in enumerate(valid_ids):
    # Try googleusercontent direct URL
    img_url = f'https://lh3.googleusercontent.com/d/{fid}'
    try:
        req = urllib.request.Request(img_url, headers={'User-Agent': 'Mozilla/5.0'})
        res = urllib.request.urlopen(req)
        data = res.read()
        if len(data) > 1000 and res.headers.get('Content-Type', '').startswith('image/'):
            ext = 'jpg' if 'jpeg' in res.headers.get('Content-Type', '') else 'png'
            out_path = os.path.join('experience_images', f'exp_img_{idx+1}.{ext}')
            with open(out_path, 'wb') as out_file:
                out_file.write(data)
            print(f"Successfully downloaded: {out_path} ({len(data)} bytes, type: {res.headers.get('Content-Type')})")
            downloaded.append((fid, out_path))
    except Exception as e:
        # Try alternate uc download link
        uc_url = f'https://drive.google.com/uc?export=download&id={fid}'
        try:
            req = urllib.request.Request(uc_url, headers={'User-Agent': 'Mozilla/5.0'})
            res = urllib.request.urlopen(req)
            data = res.read()
            if len(data) > 1000 and (data[:4] == b'\xff\xd8\xff\xe0' or data[:4] == b'\x89PNG' or b'<html' not in data[:100]):
                out_path = os.path.join('experience_images', f'exp_img_{idx+1}.jpg')
                with open(out_path, 'wb') as out_file:
                    out_file.write(data)
                print(f"Successfully downloaded via UC: {out_path} ({len(data)} bytes)")
                downloaded.append((fid, out_path))
            else:
                print(f"Skipping ID {fid}: Not image data")
        except Exception as ex:
            print(f"Failed for ID {fid}: {ex}")

print(f"\nTotal images downloaded: {len(downloaded)}")
