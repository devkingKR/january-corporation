#!/usr/bin/env python3
"""
January Corporation 웹사이트 테스트 하네스
- HTML 구조 검증
- 링크 검사 (내부/외부)
- 이미지 검사
- CSS/JS 리소스 검사
- 성능 메트릭
"""

import os
import re
import sys
import time
import json
import urllib.request
import urllib.error
from html.parser import HTMLParser
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

# 설정
BASE_DIR = Path(__file__).parent
HTML_FILES = ['index.html', 'company.html', 'business.html', 'work.html', 'newsroom.html', 'contact.html']
LOCAL_SERVER = 'http://localhost:8000'
TIMEOUT = 10

# 색상 출력
class Color:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def ok(msg): return f"{Color.GREEN}✅ {msg}{Color.END}"
def warn(msg): return f"{Color.YELLOW}⚠️  {msg}{Color.END}"
def fail(msg): return f"{Color.RED}❌ {msg}{Color.END}"
def info(msg): return f"{Color.BLUE}ℹ️  {msg}{Color.END}"
def bold(msg): return f"{Color.BOLD}{msg}{Color.END}"


class HTMLAnalyzer(HTMLParser):
    """HTML 파일 분석기"""

    def __init__(self):
        super().__init__()
        self.links = []          # href 링크
        self.images = []         # 이미지 src
        self.scripts = []        # 스크립트 src
        self.stylesheets = []    # CSS href
        self.meta_tags = []      # 메타 태그
        self.title = None
        self.has_viewport = False
        self.has_charset = False
        self.inline_styles = 0
        self.errors = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)

        if tag == 'a' and 'href' in attrs_dict:
            self.links.append(attrs_dict['href'])

        elif tag == 'img':
            if 'src' in attrs_dict:
                self.images.append({
                    'src': attrs_dict['src'],
                    'alt': attrs_dict.get('alt', None)
                })
            else:
                self.errors.append("이미지에 src 속성 누락")

        elif tag == 'script' and 'src' in attrs_dict:
            self.scripts.append(attrs_dict['src'])

        elif tag == 'link' and attrs_dict.get('rel') == 'stylesheet':
            if 'href' in attrs_dict:
                self.stylesheets.append(attrs_dict['href'])

        elif tag == 'meta':
            self.meta_tags.append(attrs_dict)
            if 'viewport' in attrs_dict.get('name', ''):
                self.has_viewport = True
            if 'charset' in attrs_dict:
                self.has_charset = True

        elif tag == 'title':
            pass  # handle_data에서 처리

        # 인라인 스타일 체크
        if 'style' in attrs_dict:
            self.inline_styles += 1

    def handle_data(self, data):
        pass


class TestHarness:
    """테스트 하네스 메인 클래스"""

    def __init__(self):
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'summary': {'total': 0, 'passed': 0, 'warnings': 0, 'failed': 0},
            'tests': []
        }
        self.server_available = False

    def add_result(self, category, name, status, message, details=None):
        """테스트 결과 추가"""
        result = {
            'category': category,
            'name': name,
            'status': status,  # 'pass', 'warn', 'fail'
            'message': message,
            'details': details or []
        }
        self.results['tests'].append(result)
        self.results['summary']['total'] += 1
        if status == 'pass':
            self.results['summary']['passed'] += 1
        elif status == 'warn':
            self.results['summary']['warnings'] += 1
        else:
            self.results['summary']['failed'] += 1

    def check_server(self):
        """로컬 서버 상태 확인"""
        print(bold("\n🔌 서버 연결 확인"))
        try:
            urllib.request.urlopen(LOCAL_SERVER, timeout=3)
            self.server_available = True
            print(ok(f"로컬 서버 연결됨: {LOCAL_SERVER}"))
            return True
        except:
            print(warn(f"로컬 서버 없음 - 파일 기반 테스트만 진행"))
            return False

    def test_html_structure(self):
        """HTML 구조 테스트"""
        print(bold("\n📄 HTML 구조 검사"))

        for filename in HTML_FILES:
            filepath = BASE_DIR / filename
            if not filepath.exists():
                self.add_result('HTML', filename, 'fail', '파일 없음')
                print(fail(f"{filename}: 파일을 찾을 수 없음"))
                continue

            content = filepath.read_text(encoding='utf-8')
            analyzer = HTMLAnalyzer()

            try:
                analyzer.feed(content)
            except Exception as e:
                self.add_result('HTML', filename, 'fail', f'파싱 오류: {e}')
                print(fail(f"{filename}: 파싱 오류"))
                continue

            issues = []

            # DOCTYPE 확인
            if not content.strip().lower().startswith('<!doctype html'):
                issues.append("DOCTYPE 누락")

            # Viewport 확인
            if not analyzer.has_viewport:
                issues.append("viewport 메타태그 누락")

            # 인라인 스타일 확인
            if analyzer.inline_styles > 0:
                issues.append(f"인라인 스타일 {analyzer.inline_styles}개")

            # 이미지 alt 속성 확인
            missing_alt = [img for img in analyzer.images if img['alt'] is None]
            if missing_alt:
                issues.append(f"alt 속성 누락 이미지 {len(missing_alt)}개")

            if issues:
                self.add_result('HTML', filename, 'warn', ', '.join(issues), issues)
                print(warn(f"{filename}: {', '.join(issues)}"))
            else:
                self.add_result('HTML', filename, 'pass', '정상')
                print(ok(f"{filename}: 구조 정상"))

    def test_links(self):
        """링크 검사"""
        print(bold("\n🔗 링크 검사"))

        all_links = set()
        internal_links = set()
        external_links = set()

        for filename in HTML_FILES:
            filepath = BASE_DIR / filename
            if not filepath.exists():
                continue

            content = filepath.read_text(encoding='utf-8')
            analyzer = HTMLAnalyzer()
            analyzer.feed(content)

            for link in analyzer.links:
                if not link or link.startswith('#') or link.startswith('javascript:'):
                    continue

                all_links.add(link)

                if link.startswith('http://') or link.startswith('https://'):
                    external_links.add(link)
                elif link.startswith('mailto:') or link.startswith('tel:'):
                    pass
                else:
                    internal_links.add(link)

        # 내부 링크 검사
        broken_internal = []
        for link in internal_links:
            # 쿼리스트링, 앵커 제거
            clean_link = link.split('?')[0].split('#')[0]
            if clean_link:
                link_path = BASE_DIR / clean_link
                if not link_path.exists():
                    broken_internal.append(clean_link)

        if broken_internal:
            self.add_result('링크', '내부 링크', 'fail', f'깨진 링크 {len(broken_internal)}개', broken_internal[:10])
            print(fail(f"깨진 내부 링크 {len(broken_internal)}개"))
            for link in broken_internal[:5]:
                print(f"    - {link}")
        else:
            self.add_result('링크', '내부 링크', 'pass', f'모든 내부 링크 정상 ({len(internal_links)}개)')
            print(ok(f"내부 링크 모두 정상 ({len(internal_links)}개)"))

        # 외부 링크 검사 (서버 있을 때만)
        if self.server_available and external_links:
            print(info(f"외부 링크 검사 중... ({len(external_links)}개)"))
            broken_external = []

            def check_url(url):
                try:
                    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                    urllib.request.urlopen(req, timeout=TIMEOUT)
                    return (url, True)
                except:
                    return (url, False)

            with ThreadPoolExecutor(max_workers=5) as executor:
                futures = {executor.submit(check_url, url): url for url in list(external_links)[:20]}
                for future in as_completed(futures):
                    url, is_valid = future.result()
                    if not is_valid:
                        broken_external.append(url)

            if broken_external:
                self.add_result('링크', '외부 링크', 'warn', f'응답 없는 외부 링크 {len(broken_external)}개', broken_external)
                print(warn(f"응답 없는 외부 링크 {len(broken_external)}개"))
            else:
                self.add_result('링크', '외부 링크', 'pass', '외부 링크 정상')
                print(ok("외부 링크 정상"))

    def test_images(self):
        """이미지 검사"""
        print(bold("\n🖼️  이미지 검사"))

        all_images = set()

        for filename in HTML_FILES:
            filepath = BASE_DIR / filename
            if not filepath.exists():
                continue

            content = filepath.read_text(encoding='utf-8')
            analyzer = HTMLAnalyzer()
            analyzer.feed(content)

            for img in analyzer.images:
                src = img['src']
                if src and not src.startswith('data:') and not src.startswith('http'):
                    all_images.add(src)

        missing_images = []
        for img_src in all_images:
            img_path = BASE_DIR / img_src
            if not img_path.exists():
                missing_images.append(img_src)

        if missing_images:
            self.add_result('이미지', '로컬 이미지', 'fail', f'누락된 이미지 {len(missing_images)}개', missing_images[:10])
            print(fail(f"누락된 이미지 {len(missing_images)}개"))
            for img in missing_images[:5]:
                print(f"    - {img}")
        else:
            self.add_result('이미지', '로컬 이미지', 'pass', f'모든 이미지 존재 ({len(all_images)}개)')
            print(ok(f"모든 이미지 존재 ({len(all_images)}개)"))

    def test_resources(self):
        """CSS/JS 리소스 검사"""
        print(bold("\n📦 리소스 검사"))

        all_css = set()
        all_js = set()

        for filename in HTML_FILES:
            filepath = BASE_DIR / filename
            if not filepath.exists():
                continue

            content = filepath.read_text(encoding='utf-8')
            analyzer = HTMLAnalyzer()
            analyzer.feed(content)

            for css in analyzer.stylesheets:
                if css and not css.startswith('http'):
                    all_css.add(css)

            for js in analyzer.scripts:
                if js and not js.startswith('http'):
                    all_js.add(js)

        # CSS 검사
        missing_css = []
        for css_src in all_css:
            css_path = BASE_DIR / css_src
            if not css_path.exists():
                missing_css.append(css_src)

        if missing_css:
            self.add_result('리소스', 'CSS', 'fail', f'누락된 CSS {len(missing_css)}개', missing_css)
            print(fail(f"누락된 CSS {len(missing_css)}개"))
            for css in missing_css:
                print(f"    - {css}")
        else:
            self.add_result('리소스', 'CSS', 'pass', f'모든 CSS 존재 ({len(all_css)}개)')
            print(ok(f"모든 CSS 존재 ({len(all_css)}개)"))

        # JS 검사
        missing_js = []
        for js_src in all_js:
            # .다운로드 같은 잘못된 파일명 체크
            if '.다운로드' in js_src or not js_src.endswith('.js'):
                missing_js.append(f"{js_src} (잘못된 파일명)")
                continue
            js_path = BASE_DIR / js_src
            if not js_path.exists():
                missing_js.append(js_src)

        if missing_js:
            self.add_result('리소스', 'JS', 'warn', f'문제 있는 JS {len(missing_js)}개', missing_js)
            print(warn(f"문제 있는 JS {len(missing_js)}개"))
            for js in missing_js:
                print(f"    - {js}")
        else:
            self.add_result('리소스', 'JS', 'pass', f'모든 JS 존재 ({len(all_js)}개)')
            print(ok(f"모든 JS 존재 ({len(all_js)}개)"))

    def test_performance(self):
        """성능 메트릭"""
        print(bold("\n⚡ 성능 메트릭"))

        total_size = 0
        file_sizes = []

        for filename in HTML_FILES:
            filepath = BASE_DIR / filename
            if filepath.exists():
                size = filepath.stat().st_size
                total_size += size
                file_sizes.append((filename, size))

        # 파일 크기 정렬
        file_sizes.sort(key=lambda x: x[1], reverse=True)

        print(f"\n  📊 HTML 파일 크기:")
        for name, size in file_sizes:
            size_kb = size / 1024
            status = "🟢" if size_kb < 50 else "🟡" if size_kb < 100 else "🔴"
            print(f"    {status} {name}: {size_kb:.1f}KB")

        avg_size = (total_size / len(HTML_FILES)) / 1024
        print(f"\n  평균 크기: {avg_size:.1f}KB")
        print(f"  총 크기: {total_size/1024:.1f}KB")

        if avg_size > 100:
            self.add_result('성능', '파일 크기', 'warn', f'평균 {avg_size:.1f}KB (목표: 50KB 이하)')
        else:
            self.add_result('성능', '파일 크기', 'pass', f'평균 {avg_size:.1f}KB')

        # 페이지 로드 테스트 (서버 있을 때)
        if self.server_available:
            print(f"\n  ⏱️  페이지 로드 시간:")
            for filename in HTML_FILES:
                start = time.time()
                try:
                    urllib.request.urlopen(f"{LOCAL_SERVER}/{filename}", timeout=10)
                    elapsed = (time.time() - start) * 1000
                    status = "🟢" if elapsed < 200 else "🟡" if elapsed < 500 else "🔴"
                    print(f"    {status} {filename}: {elapsed:.0f}ms")
                except Exception as e:
                    print(f"    🔴 {filename}: 오류")

    def test_seo(self):
        """SEO 검사"""
        print(bold("\n🔍 SEO 검사"))

        for filename in HTML_FILES:
            filepath = BASE_DIR / filename
            if not filepath.exists():
                continue

            content = filepath.read_text(encoding='utf-8')
            issues = []

            # title 태그
            if '<title>' not in content or '</title>' not in content:
                issues.append("title 태그 누락")

            # meta description
            if 'meta name="description"' not in content.lower():
                issues.append("description 메타태그 누락")

            # h1 태그
            if '<h1' not in content.lower():
                issues.append("h1 태그 누락")

            # canonical
            if 'rel="canonical"' not in content:
                issues.append("canonical 링크 누락")

            if issues:
                self.add_result('SEO', filename, 'warn', ', '.join(issues))
                print(warn(f"{filename}: {', '.join(issues)}"))
            else:
                self.add_result('SEO', filename, 'pass', 'SEO 요소 정상')
                print(ok(f"{filename}: SEO 요소 정상"))

    def run_all(self):
        """모든 테스트 실행"""
        print(bold("=" * 60))
        print(bold("🧪 January Corporation 테스트 하네스"))
        print(bold("=" * 60))
        print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        self.check_server()
        self.test_html_structure()
        self.test_links()
        self.test_images()
        self.test_resources()
        self.test_performance()
        self.test_seo()

        # 결과 요약
        print(bold("\n" + "=" * 60))
        print(bold("📋 테스트 결과 요약"))
        print(bold("=" * 60))

        summary = self.results['summary']
        print(f"  총 테스트: {summary['total']}개")
        print(f"  {Color.GREEN}통과: {summary['passed']}개{Color.END}")
        print(f"  {Color.YELLOW}경고: {summary['warnings']}개{Color.END}")
        print(f"  {Color.RED}실패: {summary['failed']}개{Color.END}")

        # JSON 결과 저장
        result_file = BASE_DIR / 'test_results.json'
        with open(result_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        print(f"\n📁 상세 결과: {result_file}")

        # 종료 코드
        if summary['failed'] > 0:
            print(fail("\n테스트 실패"))
            return 1
        elif summary['warnings'] > 0:
            print(warn("\n테스트 통과 (경고 있음)"))
            return 0
        else:
            print(ok("\n모든 테스트 통과!"))
            return 0


if __name__ == '__main__':
    harness = TestHarness()
    sys.exit(harness.run_all())
