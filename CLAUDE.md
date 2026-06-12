# Claude Code 프로젝트 가이드

이 파일은 Claude Code 및 AI 어시스턴트가 이 프로젝트를 이해하고 작업할 때 참고하는 가이드입니다.

## 프로젝트 개요

- **프로젝트**: January Corporation 공식 웹사이트
- **타입**: 정적 HTML 웹사이트 (GitHub Pages 배포)
- **도메인**: https://januarycorporation.com

## 핵심 규칙

### 절대 하지 말 것
1. HTML에 인라인 스타일(`style=""`) 추가 금지
2. jQuery Migrate 재추가 금지
3. `.다운로드` 확장자 파일 참조 금지
4. 메뉴 구조 변경 금지 (한국어·영문 페이지 모두 동일하게 유지)
5. `en/` 페이지에서 에셋을 `./`로 참조 금지 — 반드시 `../` 사용

### 반드시 할 것
1. CSS 수정은 `css/*-custom.css` 파일에서만
2. 이미지는 `wp-content/uploads/연도/월/` 폴더에 저장
3. **한국어 페이지 수정 시 `en/` 동일 페이지도 같은 커밋에서 함께 수정**
4. 수정 후 `python3 test_harness.py` 실행
5. 커밋 메시지는 한글로, 접두어 사용 (수정:, 기능:, 스타일: 등)
6. 커밋 후 `git push`까지 Claude가 직접 진행

## 파일 구조

```
주요 HTML 파일 (한국어):
├── index.html      (홈)
├── company.html    (회사소개)
├── business.html   (사업소개)
├── work.html       (포트폴리오)
├── newsroom.html   (뉴스룸)
└── contact.html    (연락처)

영문 페이지 (en/) — 한국어와 1:1 대응:
├── en/index.html
├── en/company.html
├── en/business.html
├── en/work.html
├── en/newsroom.html
└── en/contact.html

CSS 파일:
├── css/index-custom.css
├── css/company-custom.css
├── css/business-custom.css
├── css/work-custom.css
├── css/newsroom-custom.css
└── css/contact-custom.css

JS 파일:
└── wp-includes/js/jquery/jquery.min.js  (유일한 jQuery)
```

## 한/영 페이지 동기화

한국어 페이지와 `en/` 영문 페이지는 구조가 동일한 1:1 복사본입니다.
내용을 수정할 때는 **항상 양쪽을 같은 커밋에서** 수정합니다.

### en/ 경로 규칙 (자주 발생한 버그)

`en/` 폴더의 파일은 한 단계 위의 에셋을 참조하므로 경로 접두어가 다릅니다.

| 한국어 페이지 | 영문 페이지 (en/) |
|---|---|
| `./wp-content/...` | `../wp-content/...` |
| `./css/...` | `../css/...` |
| `./business/...` | `../business/...` |
| `./company.html` (페이지 간 링크) | `./company.html` (en/ 내부 기준) |

한국어 페이지에서 복사해 올 때 `./`를 `../`로 바꾸지 않으면 이미지·CSS가 깨집니다.

### 영문 페이지 수정 후 확인

- 수정한 부분에 한글이 남아 있지 않은지 확인
- 작품명·고유명사는 기존 영문 표기를 따름 (예: "Longhair Legend")

## 색상 팔레트

```css
/* 주요색 */
--primary: #667eea;      /* 파란 보라 */
--secondary: #764ba2;    /* 보라 */

/* 배경 */
--bg-header: #000000;
--bg-section: #f8f9ff;
--bg-content: #ffffff;

/* 텍스트 */
--text-heading: #000000;
--text-body: #555555;
--text-muted: #999999;
```

## 자주 하는 작업 (체크리스트)

### 히스토리 항목 추가
- [ ] `company.html` 히스토리에 항목 추가 (`<p>월. 내용 설명</p>`)
- [ ] `en/company.html` 같은 위치에 영문으로 추가
- [ ] `sitemap.xml`에서 두 페이지의 `<lastmod>`를 수정일로 갱신

### 뉴스 기사 추가
- [ ] `newsroom.html`에 한국어 기사 추가
- [ ] `en/newsroom.html`에 영문 제목 + 간략한 영문 설명 추가
- [ ] `sitemap.xml`에서 두 페이지의 `<lastmod>` 갱신

### 문구/텍스트 수정
- [ ] 한국어 페이지 수정
- [ ] `en/` 동일 페이지의 해당 부분을 영문으로 수정
- [ ] 수정 부분에 한글 잔존 여부 확인
- [ ] `sitemap.xml`에서 두 페이지의 `<lastmod>` 갱신

### 이미지 추가
```html
<!-- 한국어 페이지 -->
<p><img src="./wp-content/uploads/2026/04/파일명.jpg" alt="설명" width="300" height="200"></p>
<!-- en/ 페이지에서는 src="../wp-content/..." -->
```

### 테스트 실행
```bash
python3 test_harness.py
```

### 커밋 & 푸시
```bash
git add .
git commit -m "수정: 변경 내용"
git push
```

## 참고 문서

- `README_KO.md` - 프로젝트 전체 설명
- `POLICY.md` - 상세 코딩 규칙
- `ENGLISH_PAGES.md` - 영문 페이지(en/) 구조·관리 가이드
- `DEVELOPMENT.md` - 개발 로드맵
- `BROWSER_TEST.md` - 브라우저 테스트 체크리스트

## 주의사항

1. **배포**: `git push`하면 GitHub Pages로 자동 배포됨
2. **테스트**: 푸시 전 반드시 로컬 테스트 (`python3 -m http.server 8000`)
3. **백업**: 큰 변경 전 현재 상태 커밋해두기
