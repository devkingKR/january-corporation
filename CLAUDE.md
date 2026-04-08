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
4. 메뉴 구조 변경 금지
5. **`git push` 직접 실행 금지** — 배포는 반드시 소스트리(Sourcetree) UI를 통해 진행

### 반드시 할 것
1. CSS 수정은 `css/*-custom.css` 파일에서만
2. 이미지는 `wp-content/uploads/연도/월/` 폴더에 저장
3. 수정 후 `python3 test_harness.py` 실행
4. 커밋 메시지는 한글로, 접두어 사용 (수정:, 기능:, 스타일: 등)
5. **배포(push)는 소스트리 UI에서 직접 진행** — Claude는 커밋까지만 담당

## 파일 구조

```
주요 HTML 파일:
├── index.html      (홈)
├── company.html    (회사소개)
├── business.html   (사업소개)
├── work.html       (포트폴리오)
├── newsroom.html   (뉴스룸)
└── contact.html    (연락처)

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

## 자주 하는 작업

### 이미지 추가
```html
<p><img src="./wp-content/uploads/2026/04/파일명.jpg" alt="설명" width="300" height="200"></p>
```

### 히스토리 항목 추가 (company.html)
```html
<p>월. 내용 설명</p>
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
- `DEVELOPMENT.md` - 개발 로드맵
- `BROWSER_TEST.md` - 브라우저 테스트 체크리스트

## 주의사항

1. **배포**: `git push`하면 GitHub Pages로 자동 배포됨
2. **테스트**: 푸시 전 반드시 로컬 테스트 (`python3 -m http.server 8000`)
3. **백업**: 큰 변경 전 현재 상태 커밋해두기
