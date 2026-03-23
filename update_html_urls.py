#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
import sys

# Set UTF-8 encoding for stdout
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def update_html_file(file_path):
    """Update all januarycorporation.com URLs to local paths in an HTML file"""
    try:
        print(f"Processing: {file_path}")

        # Read the file
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # Replace URLs with local paths
        # Pattern: https://januarycorporation.com/path -> ./path or path
        # We need to be careful to preserve the structure

        # Replace wp-content, wp-includes paths with relative local paths
        content = re.sub(
            r'https://januarycorporation\.com/(wp-content/[^"\'\s>]+)',
            r'./\1',
            content
        )

        content = re.sub(
            r'https://januarycorporation\.com/(wp-includes/[^"\'\s>]+)',
            r'./\1',
            content
        )

        # Replace page links to local HTML files
        # https://januarycorporation.com/ -> ./index.html
        content = content.replace('https://januarycorporation.com/"', './index.html"')
        content = content.replace('href="https://januarycorporation.com/"', 'href="./index.html"')

        # https://januarycorporation.com/business/ -> ./business.html
        content = content.replace('https://januarycorporation.com/business/', './business.html')

        # https://januarycorporation.com/company/ -> ./company.html
        content = content.replace('https://januarycorporation.com/company/', './company.html')

        # https://januarycorporation.com/contact/ -> ./contact.html
        content = content.replace('https://januarycorporation.com/contact/', './contact.html')

        # https://januarycorporation.com/work/ -> ./work.html
        content = content.replace('https://januarycorporation.com/work/', './work.html')

        # https://januarycorporation.com/f-a-q/ -> ./newsroom.html
        content = content.replace('https://januarycorporation.com/f-a-q/', './newsroom.html')

        # Remove any remaining wp-json API references (keep as is or comment out)
        # We'll keep them as they won't work locally anyway

        # Check if content changed
        if content != original_content:
            # Backup original file
            backup_path = file_path + '.backup'
            if not os.path.exists(backup_path):
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.write(original_content)
                print(f"  [BACKUP] Created backup: {backup_path}")

            # Write updated content
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

            print(f"  [OK] Updated successfully")
            return True
        else:
            print(f"  [SKIP] No changes needed")
            return False

    except Exception as e:
        print(f"  [ERROR] Failed to update {file_path}: {e}")
        return False

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))

    print("=" * 80)
    print("January Corporation HTML URL Updater")
    print("=" * 80)
    print(f"Base directory: {base_dir}")
    print()

    # Find all HTML files
    html_files = []
    for file in os.listdir(base_dir):
        if file.endswith('.html') and not file.endswith('.backup.html'):
            html_files.append(os.path.join(base_dir, file))

    print(f"Found {len(html_files)} HTML files")
    print()

    # Update each file
    updated_count = 0
    skipped_count = 0
    failed_count = 0

    for html_file in html_files:
        result = update_html_file(html_file)
        if result:
            updated_count += 1
        elif result is False:
            skipped_count += 1
        else:
            failed_count += 1
        print()

    print("=" * 80)
    print("Update Summary")
    print("=" * 80)
    print(f"Total HTML files: {len(html_files)}")
    print(f"Updated: {updated_count}")
    print(f"Skipped: {skipped_count}")
    print(f"Failed: {failed_count}")
    print()

    if failed_count > 0:
        print("⚠ Some files failed to update.")
    else:
        print("✓ All HTML files processed successfully!")
        print()
        print("Next steps:")
        print("  1. Start a local web server (e.g., python -m http.server 8000)")
        print("  2. Open http://localhost:8000/index.html in your browser")
        print("  3. All resources should now load from local files")

if __name__ == '__main__':
    main()
