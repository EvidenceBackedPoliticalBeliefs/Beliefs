#!/usr/bin/env python3
"""
Fix markdown links to use .html extension and add base URL prefix.
This script is used during GitHub Pages deployment to ensure internal links work correctly.
"""

import re
from pathlib import Path


def fix_links_in_file(file_path):
    """Replace .md links with .html and add /Beliefs/ base URL prefix."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    def replace_link(match):
        text = match.group(1)
        url = match.group(2)
        
        # Skip external links (http://, https://, mailto:, etc.)
        if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', url):
            return match.group(0)
        
        # Skip anchors
        if url.startswith('#'):
            return match.group(0)
        
        # Replace .md with .html
        if url.endswith('.md'):
            url = url[:-3] + '.html'
        
        # Add /Beliefs/ prefix to .html links
        if '.html' in url:
            if url.startswith('/'):
                # Absolute path - add /Beliefs if not present
                if not url.startswith('/Beliefs/'):
                    url = '/Beliefs' + url
            else:
                # Relative path - make it absolute with /Beliefs
                url = '/Beliefs/' + url
        
        return f'[{text}]({url})'
    
    # Replace all markdown links [text](url)
    content = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', replace_link, content)
    
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'✓ Fixed links in: {file_path}')
    else:
        print(f'  No changes needed: {file_path}')


def main():
    """Process all markdown files in the repository."""
    print("Fixing markdown links for GitHub Pages...")
    
    # Process all markdown files
    for md_file in Path('.').rglob('*.md'):
        # Skip excluded directories
        if any(part in str(md_file) for part in ['_site', 'node_modules', '.github', 'utils']):
            continue
        fix_links_in_file(md_file)
    
    print("\nDone!")


if __name__ == '__main__':
    main()
