#!/usr/bin/env python3
"""로컬 리소스 경로 검사 스크립트.

루트 한글 페이지와 en/ 영문 페이지의 src/href/srcset 참조를 실제 파일
시스템에서 해석해 깨진 참조를 찾습니다.

잡아내는 오류:
  - en/ 페이지에서 `./wp-content/...`처럼 잘못된 접두어 사용
    (올바른 형태는 `../wp-content/...` — 파일 없음으로 검출됨)
  - 루트 페이지에서 `../...`처럼 저장소 밖을 가리키는 참조
  - 오타·이동·삭제로 깨진 이미지/CSS/JS/링크
  - 대소문자 불일치 (Windows에서는 열리지만 GitHub Pages에서는 404)

검사 제외:
  - 외부 URL (http, https, //, mailto, tel, data, javascript)
  - 페이지 내 앵커 (#...)

사용법:
  python3 check_paths.py            # 검사 실행, 발견 시 종료 코드 1
"""

import re
import sys
import urllib.parse
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).parent
SKIP_PREFIXES = ("http://", "https://", "//", "mailto:", "tel:", "data:", "javascript:")
URL_ATTRS = {"src", "href", "poster"}


def html_files():
    files = sorted(ROOT.glob("*.html")) + sorted((ROOT / "en").glob("*.html"))
    return files


class RefCollector(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.refs = []  # (line, attr, value)

    def handle_starttag(self, tag, attrs):
        line = self.getpos()[0]
        for name, value in attrs:
            if not value:
                continue
            if name in URL_ATTRS:
                self.refs.append((line, name, value))
            elif name == "srcset":
                for part in value.split(","):
                    url = part.strip().split()[0] if part.strip() else ""
                    if url:
                        self.refs.append((line, "srcset", url))


def case_mismatch(base, rel_path):
    """대소문자까지 정확히 일치하는지 확인. 불일치 시 실제 이름 반환."""
    current = base
    for part in rel_path.parts:
        if not current.is_dir():
            return None
        entries = {e.name: e.name for e in current.iterdir()}
        if part in entries:
            current = current / part
            continue
        # 대소문자만 다른 항목이 있는지 확인
        lowered = {n.lower(): n for n in entries}
        if part.lower() in lowered:
            return lowered[part.lower()]
        return None
    return None


def check_file(path):
    parser = RefCollector()
    parser.feed(path.read_text(encoding="utf-8"))
    base = path.parent
    errors = []
    for line, attr, raw in parser.refs:
        ref = raw.strip()
        if not ref or ref.startswith("#") or ref.lower().startswith(SKIP_PREFIXES):
            continue
        # 쿼리스트링·앵커 제거, 퍼센트 인코딩 복원
        ref_path = urllib.parse.unquote(ref.split("#")[0].split("?")[0])
        if not ref_path:
            continue
        target = (base / ref_path).resolve()
        try:
            rel = target.relative_to(ROOT.resolve())
        except ValueError:
            errors.append((line, attr, raw, "저장소 밖을 가리킴 (../ 과다)"))
            continue
        if not target.exists():
            hint = "파일 없음"
            if path.parent.name == "en" and ref_path.startswith("./"):
                alt = (base / ("." + ref_path)).resolve()
                if alt.exists():
                    hint = "파일 없음 — en/ 페이지는 ../ 로 참조해야 함"
            errors.append((line, attr, raw, hint))
            continue
        # 대소문자 검증 (GitHub Pages는 대소문자 구분)
        wrong = case_mismatch(ROOT.resolve(), rel)
        if wrong:
            errors.append((line, attr, raw, f"대소문자 불일치 (실제: {wrong})"))
    return errors


def main():
    total = 0
    for f in html_files():
        errors = check_file(f)
        if errors:
            name = f.relative_to(ROOT)
            print(f"\n== {name} : {len(errors)}건")
            for line, attr, raw, why in errors:
                shown = raw if len(raw) <= 80 else raw[:80] + "..."
                print(f"  {line:5d}행  [{attr}]  {shown}")
                print(f"         → {why}")
            total += len(errors)

    print()
    if total:
        print(f"깨진 경로 {total}건 발견.")
        return 1
    print("통과: 모든 로컬 리소스 경로가 정상입니다.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
