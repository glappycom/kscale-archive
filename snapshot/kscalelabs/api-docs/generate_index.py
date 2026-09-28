#!/usr/bin/env python3

import os
import re
from pathlib import Path

def title_case(s):
    """Convert string to title case, handling underscores"""
    return ' '.join(word.capitalize() for word in s.replace('_', ' ').split())

def generate_index():
    """Generate index.html from the contents of the directories"""
    # Base paths
    base_dir = Path(os.path.dirname(os.path.abspath(__file__)))
    pykos_dir = base_dir / 'pykos'
    kos_sim_dir = base_dir / 'kos_sim'
    kos_sdk_dir = base_dir / 'kos-sdk'
    
    # Get HTML files in each directory
    pykos_files = sorted([f for f in os.listdir(pykos_dir) if f.endswith('.html')]) if os.path.exists(pykos_dir) else []
    kos_sim_files = sorted([f for f in os.listdir(kos_sim_dir) if f.endswith('.html')]) if os.path.exists(kos_sim_dir) else []
    kos_sdk_files = sorted([f for f in os.listdir(kos_sdk_dir) if f.endswith('.html')]) if os.path.exists(kos_sdk_dir) else []
    
    # Generate HTML content
    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>KOS API Documentation</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        h1 {
            color: #333;
            border-bottom: 2px solid #eee;
            padding-bottom: 10px;
        }
        h2 {
            color: #444;
            margin-top: 30px;
        }
        ul {
            padding-left: 20px;
        }
        li {
            margin-bottom: 8px;
        }
        a {
            color: #0066cc;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <h1>KOS API Documentation</h1>
    
    <p>Documentation for PyKOS, KOS-Sim, and KOS-SDK.</p>
    
    <h2>PyKOS</h2>
    <ul>
"""
    
    # Add PyKOS files
    for file in pykos_files:
        name = file.replace('.html', '')
        html += f'        <li><a href="pykos/{file}">{title_case(name)}</a> - {name} service client</li>\n'
    
    if not pykos_files:
        html += '        <li>No documentation files found in the PyKOS directory.</li>\n'
    
    html += """    </ul>
    
    <h2>KOS-Sim</h2>
    <ul>
"""
    
    # Add KOS-Sim files
    for file in kos_sim_files:
        name = file.replace('.html', '')
        html += f'        <li><a href="kos_sim/{file}">{title_case(name)}</a> - {title_case(name)} documentation</li>\n'
    
    if not kos_sim_files:
        html += '        <li>No documentation files found in the KOS-Sim directory.</li>\n'
    
    html += """    </ul>
    
    <h2>KOS-SDK</h2>
    <ul>
"""
    
    # Add KOS-SDK files
    for file in kos_sdk_files:
        name = file.replace('.html', '')
        html += f'        <li><a href="kos-sdk/{file}">{title_case(name)}</a> - {title_case(name)} documentation</li>\n'
    
    if not kos_sdk_files:
        html += '        <li>No documentation files found in the KOS-SDK directory.</li>\n'
    
    html += """    </ul>
</body>
</html>
"""
    
    # Write the file
    with open(base_dir / 'index.html', 'w') as f:
        f.write(html)
    
    print("Generated index.html successfully.")

if __name__ == "__main__":
    generate_index()