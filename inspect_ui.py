with open('frontend/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()
print(f'Total lines in index.html: {len(lines)}')
for i, line in enumerate(lines):
    l_strip = line.strip()
    if any(tag in l_strip for tag in ['<header', '<footer', '<section', '<nav', 'class="modal', 'id="']):
        if any(key in l_strip for key in ['<header', '<footer', '<section', '<main', 'class="modal', 'role="main']):
            print(f'{i+1}: {l_strip[:90]}')
