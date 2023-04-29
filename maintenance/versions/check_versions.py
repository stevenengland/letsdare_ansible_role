
import glob
import os
from pathlib import Path
import re

types = (
    '**/*.yml', 
    '**/*.yaml', 
    '**/*.md'
    ) # the tuple of file types
files = []
for type in types:
    files.extend(glob.glob(os.path.dirname(__file__) + "/../../" + type, recursive=True))
    files.extend(glob.glob(os.path.dirname(__file__) + "/../../." + type, recursive=True))
    files.extend(glob.glob(os.path.dirname(__file__) + "/../../.**/" + type, recursive=True))
    #files.extend(glob.iglob(os.path.dirname(__file__) + type, recursive=True, include_hidden = True)) # ToDo: python 11 feature

files = [x for x in files if not ".venv" in x and not "molecule" in x]

ansible_versions = []
ansible_versions_files = []

for file in files:
    content = Path(file).read_text()
    matches = re.findall(r'ansible_version_minimum:\s+["\'](.*?)["\']', content)
    matches = matches + re.findall(r'min_ansible_version:\s+["\'](.*?)["\']', content)
    if len(matches) > 0:
        ansible_versions_files.append(os.path.relpath(file))
        ansible_versions = ansible_versions + matches

ansible_versions = list(set(ansible_versions))
print("Summary for minimal ansible version:")
if len(ansible_versions) > 1:
    print("[ERROR] There are multiple versions in use:")
    print(*ansible_versions, sep = "\n")
    print("Files affected:")
    print(*ansible_versions_files, sep = "\n")
else:
    print ("[PASS] Everything ok.")


letsdare_versions = []
letsdare_versions_files = []

for file in files:
    content = Path(file).read_text()
    matches = re.findall(r'letsdare_version_minimum:\s+["\'](.*?)["\']', content)
    if len(matches) > 0:
        letsdare_versions_files.append(os.path.relpath(file))
        letsdare_versions = letsdare_versions + matches

letsdare_versions = list(set(letsdare_versions))
letsdare_versions = [x for x in letsdare_versions if x not in ["99.11.0"]]
print("Summary for minimal letsdare version:")
if len(letsdare_versions) > 1:
    print("[ERROR] There are multiple versions in use:")
    print(*letsdare_versions, sep = "\n")
    print("Files affected:")
    print(*letsdare_versions_files, sep = "\n")
else:
    print ("[PASS] Everything ok.")