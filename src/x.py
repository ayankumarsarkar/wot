from pathlib import Path
import re

def match_lnk_to_dicts(directory_path, existing_dicts):
    # 1. Get all .lnk file names (without the .lnk extension)
    # Stored in a set and converted to lowercase for fast, case-insensitive comparison
    lnk_names = {path.stem.lower().strip() for path in Path(directory_path).glob('*.lnk')}

    print(lnk_names)
    matched_dicts = []

    
    # 2. Iterate through the existing dictionary list
    for entry in existing_dicts:
        name = entry.get('name', '')
        print(name)
        topic_code = re.findall(r'^[A-Z]{3}', name)
        print(topic_code)
        
        # Extract the first 3 words from the dictionary entry's name
        first_3_words = ''.join(topic_code[:3]).lower()
        print(first_3_words)
        
        # 3. Compare against the captured .lnk file names
        if first_3_words in lnk_names:
            print('processing...')
            matched_dicts.append(entry)
            print('... done!')
            
    return matched_dicts

# --- Example Usage ---

# Sample existing dictionary list
existing_data = [
    {'name': 'BFS-Basic File Server', 'type': 'local'}, 
    {'name': 'BLT-Bengali Language Transliteration', 'type': 'local'}, 
    {'name': 'CGR-Classical Greek Resources', 'type': 'local'}, 
    {'name': 'CMF-Chart of Mathematical Formulae', 'type': 'local'}, 
    {'name': 'EEL-Esper the Easiest Language', 'type': 'local'}, 
    {'name': 'PLF-Phrygia Last Frontier', 'type': 'local'}, 
    {'name': 'RIW-Reverse1999 Inspired Webpage', 'type': 'local'}, 
    {'name': 'RRC-Roguelite-Resonance-Crawler', 'type': 'local'}, 
    {'name': 'SSL-Sands on the Shore of Lucia', 'type': 'local'}, 
    {'name': 'VSP-A Very Secret Project', 'type': 'local'}, 
    {'name': 'WOT-Workflow Organising Tool', 'type': 'local'}, 
    {'name': 'WRK-Work', 'type': 'local'},
    {'name': 'TWH-And There Was War In Heaven', 'type': 'remote'}, 
    {'name': 'SOR-E̹l I̹chone̹  E̹l Rufine̹', 'type': 'remote'}, 
    {'name': 'PCS-Pleistocene Saga', 'type': 'remote'}, 
    {'name': 'TLT-A Tale Lost To Time.lnk', 'type': 'remote'}, 
    {'name': 'RRC-Roguelite-Resonance-Crawler.lnk', 'type': 'remote'}
]

# Assuming your directory has files named:
# "Google Chrome Web.lnk"
# "Visual Studio Code.lnk"
# "Random Shortcut.lnk"

matched_results = match_lnk_to_dicts(r"C:/Users/Admin/Desktop", existing_data)

for result in matched_results:
    print(result)