# 영문 페이지 가이드 (en/)

이 문서는 영문 페이지 구조, 관리 방법, 향후 작업 계획을 설명합니다.

## 디렉토리 구조

```
en/
├── index.html      (홈 영문)
├── company.html    (회사소개 영문)
├── business.html   (사업소개 영문)
├── work.html       (포트폴리오 영문)
├── newsroom.html   (뉴스룸 영문)
└── contact.html    (연락처 영문)
```

## 언어 스위처

모든 페이지 헤더 오른쪽 상단에 `KO | EN` 버튼이 표시됩니다.

- **데스크탑**: 헤더 우측에 고정 (`position: fixed`)
- **모바일**: 햄버거 메뉴 드롭다운 하단에 표시
- **스타일 파일**: `css/lang-switcher.css`

## 경로 규칙

`en/` 폴더 내 파일은 상위 폴더의 에셋을 `../`으로 참조합니다.

| 한국어 페이지 | 영문 페이지 |
|---|---|
| `./wp-content/...` | `../wp-content/...` |
| `./css/...` | `../css/...` |
| `./wp-includes/...` | `../wp-includes/...` |
| `./company.html` | `./company.html` (en/ 기준) |

## SEO 설정

각 페이지 `<head>`에 hreflang 태그가 설정되어 있습니다.

```html
<!-- 한국어 페이지에 -->
<link rel="alternate" hreflang="ko" href="https://januarycorporation.com/페이지.html"/>
<link rel="alternate" hreflang="en" href="https://januarycorporation.com/en/페이지.html"/>
<link rel="alternate" hreflang="x-default" href="https://januarycorporation.com/페이지.html"/>

<!-- 영문 페이지에 -->
<link rel="canonical" href="https://januarycorporation.com/en/페이지.html"/>
<link rel="alternate" hreflang="ko" href="https://januarycorporation.com/페이지.html"/>
<link rel="alternate" hreflang="en" href="https://januarycorporation.com/en/페이지.html"/>
```

## 영문 페이지 수정 방법

### 한국어 페이지와 함께 수정 시
한국어 원본을 수정하면 **영문 페이지도 반드시 함께 수정**해야 합니다.

1. 한국어 페이지 텍스트 수정
2. `en/` 동일 파일의 해당 텍스트 영문으로 수정
3. `sitemap.xml` 양쪽 페이지 `<lastmod>` 날짜 업데이트

### 새 뉴스 기사 추가 시 (newsroom)
1. `newsroom.html`에 한국어 기사 추가
2. `en/newsroom.html`에 영문 제목 + 간략한 영문 설명 추가
3. 기사 본문은 한국어를 그대로 두거나 영문 요약으로 대체 가능

## 향후 작업 계획

### Phase 2: 브라우저 언어 자동 감지
루트 `index.html`에 JS를 추가하여 브라우저 언어 설정에 따라 자동 리다이렉트합니다.

```javascript
// index.html 상단 <script>에 추가 예정
const lang = navigator.language || navigator.userLanguage;
if (lang && lang.startsWith('en') && !sessionStorage.getItem('lang-chosen')) {
    sessionStorage.setItem('lang-chosen', 'en');
    window.location.replace('./en/index.html');
}
```

- 한국어 브라우저 → `januarycorporation.com/` (현재 동작)
- 영어 브라우저 → `januarycorporation.com/en/` 자동 이동
- 수동으로 KO/EN 선택 시 → `sessionStorage`에 기록하여 재리다이렉트 방지

> 이 기능은 별도 요청 시 구현합니다.

## 커밋 메시지 예시

```
기능: en/newsroom.html 신규 기사 추가
수정: en/company.html 히스토리 항목 업데이트
스타일: css/lang-switcher.css 모바일 위치 조정
```
