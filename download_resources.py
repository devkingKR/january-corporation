#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import urllib.request
import urllib.parse
from pathlib import Path
import time
import sys

# Set UTF-8 encoding for stdout
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def download_file(url, local_path):
    """Download a file from URL to local path"""
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(local_path), exist_ok=True)

        # Skip if file already exists
        if os.path.exists(local_path):
            print(f"  [SKIP] Already exists: {local_path}")
            return True

        # Download the file
        print(f"  [DOWN] {url}")
        print(f"    -> {local_path}")

        # Properly encode URL - parse and re-encode the path component only
        parsed = urllib.parse.urlparse(url)
        # Quote the path, but safe characters like / should not be quoted
        encoded_path = urllib.parse.quote(parsed.path.encode('utf-8'), safe='/:@!$&\'()*+,;=')
        # Reconstruct URL
        encoded_url = urllib.parse.urlunparse((
            parsed.scheme, parsed.netloc, encoded_path,
            parsed.params, parsed.query, parsed.fragment
        ))

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        req = urllib.request.Request(encoded_url, headers=headers)

        with urllib.request.urlopen(req, timeout=30) as response:
            with open(local_path, 'wb') as out_file:
                out_file.write(response.read())

        print(f"  [OK] Downloaded successfully")
        time.sleep(0.5)  # Be nice to the server
        return True

    except Exception as e:
        print(f"  [ERROR] Failed to download {url}: {e}")
        return False

def should_download(url):
    """Check if URL should be downloaded"""
    # Skip these patterns
    skip_patterns = [
        'wp-json/',
        'wp-admin/',
        '?p=',
        '#',
        'oembed',
        'admin-ajax.php'
    ]

    for pattern in skip_patterns:
        if pattern in url:
            return False

    # Only download actual files
    if url.endswith('/'):
        return False

    return True

def url_to_local_path(url, base_dir):
    """Convert URL to local file path"""
    # Remove the base URL
    path = url.replace('https://januarycorporation.com/', '')

    # Decode URL encoding
    path = urllib.parse.unquote(path)

    # Create full local path
    local_path = os.path.join(base_dir, path)

    return local_path

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    urls_file = os.path.join(base_dir, 'external_urls.txt')

    print("=" * 80)
    print("January Corporation Resource Downloader")
    print("=" * 80)
    print(f"Base directory: {base_dir}")
    print(f"Reading URLs from: {urls_file}")
    print()

    # Read URLs from file
    with open(urls_file, 'r', encoding='utf-8') as f:
        urls = [line.strip() for line in f if line.strip()]

    print(f"Total URLs found: {len(urls)}")
    print()

    # Filter URLs to download
    download_urls = [url for url in urls if should_download(url)]
    print(f"URLs to download: {len(download_urls)}")
    print()

    # Download each file
    success_count = 0
    fail_count = 0
    skip_count = len(urls) - len(download_urls)

    for i, url in enumerate(download_urls, 1):
        print(f"[{i}/{len(download_urls)}] Processing: {url}")
        local_path = url_to_local_path(url, base_dir)

        if download_file(url, local_path):
            success_count += 1
        else:
            fail_count += 1
        print()

    print("=" * 80)
    print("Download Summary")
    print("=" * 80)
    print(f"Total URLs: {len(urls)}")
    print(f"Skipped: {skip_count}")
    print(f"Downloaded: {success_count}")
    print(f"Failed: {fail_count}")
    print()

    if fail_count > 0:
        print("⚠ Some files failed to download. You may need to retry.")
    else:
        print("✓ All files downloaded successfully!")

if __name__ == '__main__':
    main()
