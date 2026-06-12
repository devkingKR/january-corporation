#!/usr/bin/env python3
"""영문 페이지(en/) 잔여 한글 검사 스크립트.

en/*.html에서 사용자에게 노출되는 한글을 찾아 보고합니다.

검사 대상:
  - 텍스트 노드 (화면에 표시되는 본문)
  - 접근성/표시 속성: alt, title, aria-label, placeholder

검사 제외:
  - <script>, <style> 내용 (JSON-LD 구조화 데이터 등)
  - HTML 주석
  - 경로/URL 속성 (src, href, content 등 — 한글 파일명은 정상)
  - korean_allowlist.txt에 등록된 의도적 한글 (한국어 곡명·작품명 등)

사용법:
  python3 check_korean.py            # 검사 실행, 발견 시 종료 코드 1
  python3 check_korean.py --list     # 허용 목록 무시하고 전체 한글 출력

허용 목록(korean_allowlist.txt): 한 줄에 하나씩, 해당 문자열을 포함한
발견 항목은 통과 처리. '#'으로 시작하는 줄은 주석.
'='으로 시작하는 줄은 발견 항목 전체가 정확히 일치할 때만 통과
(짧은 단어가 다른 문장까지 가리는 것을 방지).
"""

import re
import sys
from html.parser import HTMLParser
from pathlib import Path

KOREAN_RE = re.compile(r"[가-힣ㄱ-ㅎㅏ-ㅣ]+")
CHECKED_ATTRS = {"alt", "title", "aria-label", "placeholder"}
EN_DIR = Path(__file__).parent / "en"
ALLOWLIST_FILE = Path(__file__).parent / "korean_allowlist.txt"


def load_allowlist():
    if not ALLOWLIST_FILE.exists():
        return []
    entries = []
    for line in ALLOWLIST_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            entries.append(line)
    return entries


class KoreanFinder(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.findings = []  # (line, kind, snippet)
        self._skip_depth = 0  # script/style 내부 여부

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self._skip_depth += 1
        for name, value in attrs:
            if value and name in CHECKED_ATTRS and KOREAN_RE.search(value):
                line = self.getpos()[0]
                self.findings.append((line, f'{name}="..."', value.strip()))

    def handle_endtag(self, tag):
        if tag in ("script", "style") and self._skip_depth > 0:
            self._skip_depth -= 1

    def handle_data(self, data):
        if self._skip_depth:
            return
        if KOREAN_RE.search(data):
            line = self.getpos()[0]
            self.findings.append((line, "텍스트", " ".join(data.split())))


def is_allowed(snippet, allowlist):
    for allowed in allowlist:
        if allowed.startswith("="):
            if snippet == allowed[1:]:
                return True
        elif allowed in snippet:
            return True
    return False


def check_file(path, allowlist, show_all=False):
    parser = KoreanFinder()
    parser.feed(path.read_text(encoding="utf-8"))
    results = []
    for line, kind, snippet in parser.findings:
        if not show_all and is_allowed(snippet, allowlist):
            continue
        results.append((line, kind, snippet))
    return results


def main():
    show_all = "--list" in sys.argv
    allowlist = load_allowlist()

    files = sorted(EN_DIR.glob("*.html"))
    if not files:
        print(f"오류: {EN_DIR} 에서 HTML 파일을 찾지 못했습니다.")
        return 2

    total = 0
    for f in files:
        results = check_file(f, allowlist, show_all)
        if results:
            print(f"\n== en/{f.name} : {len(results)}건")
            for line, kind, snippet in results:
                if len(snippet) > 90:
                    snippet = snippet[:90] + "..."
                print(f"  {line:5d}행  [{kind}]  {snippet}")
            total += len(results)

    print()
    if total:
        print(f"잔여 한글 {total}건 발견. 영문으로 수정하거나, 의도된 한글이면")
        print(f"korean_allowlist.txt에 해당 문자열을 추가하세요.")
        return 1
    print("통과: 영문 페이지에 잔여 한글이 없습니다.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
