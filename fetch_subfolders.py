import urllib.request
import re
import os
import shutil

folders = {
    'experinces': '1T5SJXy1xc-34s1R76lhPW7amiBXrkfWm',
    'projects': '1a0njhsLBbBE2KLDbKaFm2gsZU9ORNzzj'
}

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

for f_name, f_id in folders.items():
    url = f'https://drive.google.com/drive/folders/{f_id}'
    os.makedirs(os.path.join('d:\\diya portfolio', f_name), exist_ok=True)
    print(f"\n--- Fetching subfolder: {f_name} ({f_id}) ---")
    try:
        req = urllib.request.Request(url, headers=headers)
        html = urllib.request.urlopen(req).read().decode('utf-8', errors='ignore')
        
        # Save HTML for inspection
        with open(f'{f_name}_page.html', 'w', encoding='utf-8') as out:
            out.write(html)
            
        # Match pattern: ["FILE_ID", ["FILENAME"]] or similar Drive JS arrays
        matches = re.findall(r'\["([1a-zA-Z0-9_-]{25,35})",\s*\["([^"]+)"', html)
        print(f"Found {len(matches)} matches in {f_name}:")
        
        for fid, fname in matches:
            print(f"File ID: {fid} | Name: {fname}")
            # Attempt to download thumbnail / image file
            thumb_url = f"https://lh3.googleusercontent.com/d/{fid}"
            try:
                t_req = urllib.request.Request(thumb_url, headers=headers)
                t_res = urllib.request.urlopen(t_req)
                t_data = t_res.read()
                if len(t_data) > 1000:
                    clean_fname = re.sub(r'[^\w\.-]', '_', fname)
                    if not clean_fname.endswith(('.png', '.jpg', '.jpeg')):
                        clean_fname += '.png'
                    file_path = os.path.join('d:\\diya portfolio', f_name, clean_fname)
                    with open(file_path, 'wb') as f_out:
                        f_out.write(t_data)
                    print(f" -> Saved {clean_fname} ({len(t_data)} bytes)")
            except Exception as ex:
                print(f" -> Download failed for {fid}: {ex}")
                
    except Exception as e:
        print(f"Error fetching {f_name}: {e}")
