#!/usr/bin/env python3
"""
JS 경로 수정 스크립트
- .다운로드 확장자 제거
- 올바른 wp-content/wp-includes 경로로 변경
"""

import re
from pathlib import Path

# 경로 매핑 (잘못된 파일명 -> 올바른 경로)
PATH_MAPPINGS = {
    'jquery.min.js': './wp-includes/js/jquery/jquery.min.js',
    'imagesloaded.min.js': './wp-includes/js/imagesloaded.min.js',
    'theme.min.js': './wp-content/themes/oceanwp/assets/js/theme.min.js',
    'full-screen-menu.min.js': './wp-content/themes/oceanwp/assets/js/full-screen-menu.min.js',
    'drop-down-mobile-menu.min.js': './wp-content/themes/oceanwp/assets/js/drop-down-mobile-menu.min.js',
    'drop-down-search.min.js': './wp-content/themes/oceanwp/assets/js/drop-down-search.min.js',
    'magnific-popup.min.js': './wp-content/themes/oceanwp/assets/js/vendors/magnific-popup.min.js',
    'ow-lightbox.min.js': './wp-content/themes/oceanwp/assets/js/ow-lightbox.min.js',
    'flickity.pkgd.min.js': './wp-content/themes/oceanwp/assets/js/vendors/flickity.pkgd.min.js',
    'ow-slider.min.js': './wp-content/themes/oceanwp/assets/js/ow-slider.min.js',
    'scroll-effect.min.js': './wp-content/themes/oceanwp/assets/js/scroll-effect.min.js',
    'scroll-top.min.js': './wp-content/themes/oceanwp/assets/js/scroll-top.min.js',
    'select.min.js': './wp-content/themes/oceanwp/assets/js/select.min.js',
    'webpack.runtime.min.js': './wp-content/plugins/elementor/assets/js/webpack.runtime.min.js',
    'frontend-modules.min.js': './wp-content/plugins/elementor/assets/js/frontend-modules.min.js',
    'waypoints.min.js': './wp-content/plugins/elementor/assets/lib/waypoints/waypoints.min.js',
    'core.min.js': './wp-includes/js/jquery/ui/core.min.js',
    'swiper.min.js': './wp-content/plugins/elementor/assets/lib/swiper/swiper.min.js',
    'share-link.min.js': './wp-content/plugins/elementor/assets/lib/share-link/share-link.min.js',
    'dialog.min.js': './wp-content/plugins/elementor/assets/lib/dialog/dialog.min.js',
    'frontend.min.js': './wp-content/plugins/elementor/assets/js/frontend.min.js',
    'preloaded-modules.min.js': './wp-content/plugins/elementor/assets/js/preloaded-modules.min.js',
}

def fix_js_paths(html_file):
    """HTML 파일의 잘못된 JS 경로 수정"""
    filepath = Path(html_file)
    content = filepath.read_text(encoding='utf-8')
    original_content = content

    fixes = []

    # .다운로드 패턴 찾기 및 수정
    # 예: ./business/jquery.min.js.다운로드 -> ./wp-includes/js/jquery/jquery.min.js
    pattern = r'\./(?:business|contact|newsroom)/([a-zA-Z0-9._-]+\.min\.js)\.다운로드'

    def replace_path(match):
        filename = match.group(1)
        if filename in PATH_MAPPINGS:
            new_path = PATH_MAPPINGS[filename]
            fixes.append(f"  {match.group(0)} -> {new_path}")
            return new_path
        else:
            fixes.append(f"  ⚠️ 매핑 없음: {filename}")
            return match.group(0)

    content = re.sub(pattern, replace_path, content)

    if content != original_content:
        filepath.write_text(content, encoding='utf-8')
        print(f"✅ {html_file} 수정 완료 ({len(fixes)}개)")
        for fix in fixes:
            print(fix)
    else:
        print(f"ℹ️ {html_file} 변경 없음")

    return len(fixes)

def main():
    print("🔧 JS 경로 수정 시작\n")

    files_to_fix = ['business.html', 'contact.html', 'newsroom.html']
    total_fixes = 0

    for html_file in files_to_fix:
        if Path(html_file).exists():
            total_fixes += fix_js_paths(html_file)
            print()
        else:
            print(f"❌ {html_file} 파일 없음\n")

    print(f"✅ 총 {total_fixes}개 경로 수정 완료")

if __name__ == '__main__':
    main()
