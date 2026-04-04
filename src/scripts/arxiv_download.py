#!/usr/bin/env python3
"""Download a paper from arxiv by ID or URL.

Usage:
    python3 arxiv_download.py 2301.12345
    python3 arxiv_download.py 2301.12345v2
    python3 arxiv_download.py https://arxiv.org/abs/2301.12345
    python3 arxiv_download.py hep-th/0601001

Saves PDF to refs/ARXIV_ID.pdf relative to the project root.
"""
import sys
import re
import os
import urllib.request
import urllib.error


def find_project_root():
    """Walk up from this script to find the project root (contains CLAUDE.md)."""
    current = os.path.dirname(os.path.abspath(__file__))
    while current != os.path.dirname(current):
        if os.path.exists(os.path.join(current, 'CLAUDE.md')):
            return current
        current = os.path.dirname(current)
    # Fallback: two levels up from src/scripts/
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def extract_id(input_str):
    """Extract arxiv ID from URL or bare ID string."""
    input_str = input_str.strip()
    patterns = [
        r'arxiv\.org/(?:abs|pdf)/(.+?)(?:\.pdf)?(?:\?.*)?$',
        r'^(\d{4}\.\d{4,5}(?:v\d+)?)$',
        r'^([a-z-]+/\d{7}(?:v\d+)?)$',
    ]
    for p in patterns:
        m = re.search(p, input_str)
        if m:
            return m.group(1)
    return input_str


def download(arxiv_id):
    project_root = find_project_root()
    refs_dir = os.path.join(project_root, 'refs')
    os.makedirs(refs_dir, exist_ok=True)

    safe_name = arxiv_id.replace('/', '_')
    outpath = os.path.join(refs_dir, f'{safe_name}.pdf')

    if os.path.exists(outpath):
        print(f'Already exists: {outpath}')
        return outpath

    url = f'https://arxiv.org/pdf/{arxiv_id}.pdf'
    print(f'Downloading {url} ...')
    try:
        urllib.request.urlretrieve(url, outpath)
    except urllib.error.HTTPError as e:
        print(f'Error: HTTP {e.code} for {url}')
        sys.exit(1)
    print(f'Saved: {outpath}')
    return outpath


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    arxiv_id = extract_id(sys.argv[1])
    download(arxiv_id)
