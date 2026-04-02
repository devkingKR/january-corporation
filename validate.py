#!/usr/bin/env python3
"""
January Corporation 자동 검증 스크립트
모든 HTML 파일의 기술적 문제를 자동으로 검사하고 리포트 생성
"""

import os
import re
from pathlib import Path
from datetime import datetime

BASE_PATH = Path('/Users/JHLEE/january-corporation')
HTML_FILES = [
    'index.html',
    'company.html',
    'business.html',
    'work.html',
    'newsroom.html',
    'contact.html'
]

class HTMLValidator:
    def __init__(self, file_path):
        self.file_path = file_path
        self.file_name = file_path.name
        self.file_size = file_path.stat().st_size / 1024  # KB

        with open(file_path, 'r', encoding='utf-8') as f:
            self.content = f.read()

    def check_jquery_migrate(self):
        """jQuery Migrate 확인"""
        return 'jquery-migrate' in self.content

    def check_custom_css(self):
        """커스텀 CSS 파일 링크 확인"""
        css_name = self.file_name.replace('.html', '-custom.css')
        return css_name in self.content

    def check_viewport(self):
        """Viewport meta tag 확인"""
        return 'viewport' in self.content

    def check_menu_contact(self):
        """메뉴에 CONTACT 있는지 확인"""
        # 데스크탑 메뉴와 모바일 메뉴 모두 확인
        desktop_contact = 'menu-item-2646' in self.content and 'CONTACT' in self.content
        return desktop_contact

    def check_media_queries(self):
        """반응형 미디어쿼리 확인"""
        media_queries = re.findall(r'@media.*?\{', self.content)
        return len(media_queries) > 0

    def check_inline_styles(self):
        """인라인 스타일 확인 (style="..." 형태)"""
        # 스크립트 태그 내 인라인 스타일은 제외
        inline_count = len(re.findall(r'style="[^"]*"', self.content))
        return inline_count

    def check_broken_links(self):
        """깨진 상대 경로 확인"""
        issues = []

        # .html 링크 확인
        html_links = re.findall(r'href="([^"]*\.html)"', self.content)
        for link in html_links:
            if link.startswith('./'):
                continue
            if not link.startswith('http') and link.endswith('.html'):
                issues.append(f"상대 경로 누락: {link}")

        return issues

    def check_css_links(self):
        """CSS 파일 링크 확인"""
        css_links = re.findall(r'href="([^"]*\.css)"', self.content)
        missing = []

        for link in css_links:
            # ./css/ 형태가 아니면 플래그
            if 'css/' in link and not link.startswith('./'):
                missing.append(f"상대 경로 누락: {link}")

        return missing

    def count_lines(self):
        """총 라인 수"""
        return len(self.content.split('\n'))

    def validate(self):
        """모든 검증 실행"""
        return {
            'file_name': self.file_name,
            'file_size_kb': round(self.file_size, 1),
            'total_lines': self.count_lines(),
            'has_jquery_migrate': self.check_jquery_migrate(),
            'has_custom_css': self.check_custom_css(),
            'has_viewport': self.check_viewport(),
            'has_contact_menu': self.check_menu_contact(),
            'has_media_queries': self.check_media_queries(),
            'inline_style_count': self.check_inline_styles(),
            'broken_relative_paths': self.check_broken_links(),
            'missing_css_paths': self.check_css_links(),
        }

def generate_report(results):
    """마크다운 리포트 생성"""
    report = []
    report.append("# January Corporation 자동 검증 리포트\n")
    report.append(f"**생성 시간**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    report.append("---\n")

    # 요약
    report.append("## 📊 검증 요약\n")

    total_files = len(results)
    good_files = sum(1 for r in results if is_perfect(r))
    warning_files = sum(1 for r in results if has_warnings(r))

    report.append(f"- **총 파일**: {total_files}개\n")
    report.append(f"- **정상**: {good_files}개 ✅\n")
    report.append(f"- **경고**: {warning_files}개 ⚠️\n")
    report.append("\n")

    # 상세 결과
    report.append("## 📋 파일별 상세 결과\n\n")

    for result in results:
        report.append(f"### {result['file_name']}\n")
        report.append(f"- **파일 크기**: {result['file_size_kb']}KB\n")
        report.append(f"- **라인 수**: {result['total_lines']:,}줄\n\n")

        # 체크 항목
        checks = [
            ("jQuery Migrate 제거됨", not result['has_jquery_migrate']),
            ("커스텀 CSS 링크됨", result['has_custom_css']),
            ("Viewport 설정됨", result['has_viewport']),
            ("메뉴 CONTACT 적용됨", result['has_contact_menu']),
            ("반응형 미디어쿼리", result['has_media_queries']),
        ]

        for check_name, is_good in checks:
            status = "✅" if is_good else "❌"
            report.append(f"{status} {check_name}\n")

        # 경고
        report.append("\n")
        if result['inline_style_count'] > 0:
            report.append(f"⚠️ **경고**: 인라인 스타일 {result['inline_style_count']}개 발견\n")

        if result['broken_relative_paths']:
            report.append("⚠️ **경고**: 상대 경로 문제\n")
            for issue in result['broken_relative_paths']:
                report.append(f"  - {issue}\n")

        if result['missing_css_paths']:
            report.append("⚠️ **경고**: CSS 경로 문제\n")
            for issue in result['missing_css_paths']:
                report.append(f"  - {issue}\n")

        report.append("\n---\n\n")

    # 권장사항
    report.append("## 💡 권장사항\n\n")

    jquery_migrate_files = [r['file_name'] for r in results if r['has_jquery_migrate']]
    if jquery_migrate_files:
        report.append(f"### jQuery Migrate 제거 필요\n")
        report.append("다음 파일에서 제거하세요:\n")
        for f in jquery_migrate_files:
            report.append(f"- `{f}`\n")
        report.append("\n")

    no_custom_css = [r['file_name'] for r in results if not r['has_custom_css']]
    if no_custom_css:
        report.append(f"### 커스텀 CSS 파일 연결 필요\n")
        report.append("다음 파일에 커스텀 CSS를 링크하세요:\n")
        for f in no_custom_css:
            css_name = f.replace('.html', '-custom.css')
            report.append(f"- `{f}` → `{css_name}`\n")
        report.append("\n")

    report.append("\n---\n\n")
    report.append("## 🧪 다음 단계: 수동 브라우저 테스트\n\n")
    report.append("BROWSER_TEST.md 참고하여 다음을 확인하세요:\n")
    report.append("1. **모바일 Safari** (iPhone)\n")
    report.append("2. **모바일 Chrome** (Android)\n")
    report.append("3. **데스크톱 Chrome**\n")
    report.append("4. **데스크톱 Edge**\n")

    return ''.join(report)

def is_perfect(result):
    """파일이 완벽한지 확인"""
    return (
        not result['has_jquery_migrate'] and
        result['has_custom_css'] and
        result['has_viewport'] and
        result['has_contact_menu'] and
        result['has_media_queries'] and
        result['inline_style_count'] == 0 and
        len(result['broken_relative_paths']) == 0
    )

def has_warnings(result):
    """파일이 경고가 있는지 확인"""
    return not is_perfect(result)

def main():
    print("🔍 January Corporation 자동 검증 시작...\n")

    results = []

    for html_file in HTML_FILES:
        file_path = BASE_PATH / html_file

        if not file_path.exists():
            print(f"⚠️  {html_file} 파일을 찾을 수 없습니다.")
            continue

        print(f"📄 검사 중: {html_file}...", end='')
        validator = HTMLValidator(file_path)
        result = validator.validate()
        results.append(result)
        print(" ✅")

    # 리포트 생성
    report = generate_report(results)

    # 리포트 파일 저장
    report_path = BASE_PATH / 'VALIDATION_REPORT.md'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"\n✅ 검증 완료!")
    print(f"📋 리포트: {report_path}")
    print(f"\n{report}")

if __name__ == '__main__':
    main()
