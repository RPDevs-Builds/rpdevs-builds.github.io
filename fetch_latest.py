import urllib.request
import json
import re
import os

repo_url = "https://api.github.com/repos/RPDevs-Vault/repository.rpdev/contents/omega/zips/repository.rpdevs"
try:
    headers = {"Accept": "application/vnd.github.v3+json"}
    if "GITHUB_TOKEN" in os.environ:
        headers["Authorization"] = f"token {os.environ['GITHUB_TOKEN']}"
        
    req = urllib.request.Request(repo_url, headers=headers)
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
        
    zips = [item for item in data if item['name'].endswith('.zip')]
    if not zips:
        print("No zip found.")
        exit(1)
        
    # Sort by version (descending) assuming format repository.rpdevs-X.Y.Z.zip
    def extract_version(name):
        match = re.search(r'-(\d+\.\d+\.\d+)', name)
        if match:
            return [int(x) for x in match.group(1).split('.')]
        return [0, 0, 0]
        
    latest_zip = sorted(zips, key=lambda x: extract_version(x['name']), reverse=True)[0]
    
    zip_name = latest_zip['name']
    zip_url = latest_zip['download_url']
    
    print(f"Downloading {zip_name} from {zip_url}...")
    urllib.request.urlretrieve(zip_url, zip_name)
    
    # Update index.html
    with open('index.html', 'r') as f:
        html = f.read()
        
    # Replace the link in index.html
    html = re.sub(r'<a href="[^"]+">repository\.rpdevs-[^<]+</a>', f'<a href="{zip_name}">{zip_name}</a>', html)
    
    with open('index.html', 'w') as f:
        f.write(html)
        
    print(f"Successfully updated to {zip_name}")
except Exception as e:
    print(f"Error: {e}")
    exit(1)
