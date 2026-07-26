import re
import os
import urllib.request

for f_name in ['experinces', 'projects']:
    h_file = f'{f_name}_page.html'
    if not os.path.exists(h_file):
        continue
    with open(h_file, 'r', encoding='utf-8') as f:
        text = f.read()
    
    print(f"\n================ Inspecting {h_file} ================")
    # Look for any occurrence of "Screenshot"
    sc_matches = re.findall(r'Screenshot[^\"]*', text)
    print(f"Screenshot filename occurrences ({len(sc_matches)}):")
    for m in sc_matches[:15]:
        print("  -", m)
        
    # Find surrounding context for "Screenshot"
    pos = 0
    ids_found = []
    while True:
        pos = text.find('Screenshot', pos)
        if pos == -1:
            break
        # grab surrounding 300 chars
        snippet = text[max(0, pos-200):min(len(text), pos+200)]
        # look for candidate Google Drive IDs (28-35 alphanumeric chars) in snippet
        candidate_ids = re.findall(r'1[a-zA-Z0-9_-]{28,34}', snippet)
        for cid in candidate_ids:
            if cid not in ids_found and len(cid) >= 28:
                ids_found.append(cid)
                print(f"Found ID {cid} near snippet: {snippet[:80]}...")
        pos += 10

    print(f"Total candidate file IDs for {f_name}: {len(ids_found)}")
    
    # Download images using candidates
    headers = {'User-Agent': 'Mozilla/5.0'}
    for idx, fid in enumerate(ids_found):
        url = f"https://lh3.googleusercontent.com/d/{fid}"
        try:
            req = urllib.request.Request(url, headers=headers)
            res = urllib.request.urlopen(req)
            data = res.read()
            if len(data) > 1000 and (b'PNG' in data[:10] or b'JFIF' in data[:20] or b'Exif' in data[:20]):
                out_path = os.path.join('d:\\diya portfolio', f_name, f'item_{idx+1}.png')
                with open(out_path, 'wb') as out_f:
                    out_f.write(data)
                print(f" ==> DOWNLOADED: {out_path} ({len(data)} bytes)")
        except Exception as e:
            pass
