import urllib.request
import re
import os

main_url = "https://drive.google.com/drive/folders/1AGu61KNI10AM-9g30R2wi6rHBB4gUE7_?usp=sharing"
req = urllib.request.Request(main_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
html = urllib.request.urlopen(req).read().decode('utf-8')

# Find all file ID patterns in drive
file_patterns = re.findall(r'\["([a-zA-Z0-9_-]{28,35})",\["([^"]+)"', html)
print(f"Found {len(file_patterns)} raw items")

# Look specifically for projects folder ID
folder_patterns = re.findall(r'\["([a-zA-Z0-9_-]{28,35})","(projects|experinces|profile photo)"', html, re.IGNORECASE)
print("Folders found:", folder_patterns)

for folder_id, folder_name in folder_patterns:
    if folder_name.lower() == "projects":
        print(f"\nScanning projects folder ID: {folder_id}")
        proj_url = f"https://drive.google.com/drive/folders/{folder_id}"
        req2 = urllib.request.Request(proj_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        p_html = urllib.request.urlopen(req2).read().decode('utf-8')
        
        # Extract files in projects folder
        p_files = re.findall(r'\["([a-zA-Z0-9_-]{28,35})",\["([^"]+)"', p_html)
        print(f"Found {len(p_files)} items in projects folder:")
        
        out_dir = r"d:\diya portfolio\assets\projects_hd"
        os.makedirs(out_dir, exist_ok=True)
        
        count = 0
        seen_ids = set()
        for fid, fname in p_files:
            if fid not in seen_ids and ("." in fname or "Screenshot" in fname or "PNG" in fname or "JPG" in fname or "proj" in fname):
                seen_ids.add(fid)
                count += 1
                dl_url = f"https://lh3.googleusercontent.com/d/{fid}=w3840-h2160" # Maximum HD quality render endpoint!
                print(f"Downloading HD [{count}] {fname} (ID: {fid})...")
                out_path = os.path.join(out_dir, f"hd_proj_{count}.png")
                try:
                    urllib.request.urlretrieve(dl_url, out_path)
                    print(f"  -> Saved {out_path} ({os.path.getsize(out_path)} bytes)")
                except Exception as e:
                    print(f"  -> Error: {e}")
