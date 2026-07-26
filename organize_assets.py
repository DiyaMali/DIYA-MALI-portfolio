import os
import shutil
import re

os.makedirs(r'd:\diya portfolio\assets\experiences', exist_ok=True)
os.makedirs(r'd:\diya portfolio\assets\projects', exist_ok=True)

# Copy hero portrait
src_hero = r'd:\diya portfolio\diya_portrait.jpg'
dst_hero = r'd:\diya portfolio\assets\diya_portrait.jpg'
if os.path.exists(src_hero):
    shutil.copyfile(src_hero, dst_hero)
    print("Copied hero portrait to assets/diya_portrait.jpg")

# Copy experience images
exp_dir = r'd:\diya portfolio\experinces'
exp_files = [f for f in os.listdir(exp_dir) if f.endswith(('.png', '.jpg'))]

def extract_num(val):
    nums = re.findall(r'\d+', val)
    return int(nums[0]) if nums else 0

exp_files.sort(key=extract_num)

for idx, f in enumerate(exp_files):
    src = os.path.join(exp_dir, f)
    dst = os.path.join(r'd:\diya portfolio\assets\experiences', f'exp_{idx+1}.png')
    shutil.copyfile(src, dst)
    print(f"Experience image {idx+1}: {dst}")

# Copy project images
proj_dir = r'd:\diya portfolio\projects'
proj_files = [f for f in os.listdir(proj_dir) if f.endswith(('.png', '.jpg'))]
proj_files.sort(key=extract_num)

for idx, f in enumerate(proj_files):
    src = os.path.join(proj_dir, f)
    dst = os.path.join(r'd:\diya portfolio\assets\projects', f'proj_{idx+1}.png')
    shutil.copyfile(src, dst)
    print(f"Project image {idx+1}: {dst}")

print("\nAssets successfully organized!")
