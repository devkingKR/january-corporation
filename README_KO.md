# January Corporation 웹사이트

## 📌 개요

January Corporation(제뉴어리코퍼레이션)의 공식 웹사이트입니다.

- **회사명**: January Corporation
- **사업**: K-콘텐츠 엔터테크 스튜디오
- **웹사이트**: [januarycorporation.com](https://januarycorporation.com)

---

## 🛠️ 기술 스택

| 레이어 | 기술 |
|-------|------|
| 마크업 | HTML5 |
| 스타일 | CSS3 + Responsive Design |
| 스크립트 | jQuery 3.x |
| 아이콘 | Font Awesome |
| 테마 | OceanWP (기반) |

---

## 📂 프로젝트 구조

```
january-corporation/
├── index.html              # 홈페이지
├── company.html            # 회사소개
├── business.html           # 사업소개
├── work.html              # 포트폴리오
├── newsroom.html          # 뉴스룸
├── contact.html           # 연락처
│
├── css/
│   ├── fontawesome-all.min.css
│   ├── simple-line-icons.min.css
│   ├── oceanwp-style.css
│   ├── widgets.css
│   ├── *-custom.css       # 페이지별 커스텀 스타일
│   └── global.css
│
├── js/
│   └── jquery/
│       └── jquery.min.js
│
├── images/                # 이미지 리소스
├── webfonts/             # 웹 폰트
├── fonts/                # 아이콘 폰트
└── wp-content/           # WordPress 테마/플러그인
```

---

## 🎨 디자인 시스템

### 색상 팔레트
```
주요색:
- Purple-Blue (#667eea)
- Deep Purple (#764ba2)

중립색:
- Black (#000000)
- Dark Gray (#333333)
- Medium Gray (#555555)
- Light Gray (#999999)

배경색:
- Header (#000000)
- Section (#f8f9ff)
- Content (#ffffff)
```

### 반응형 디자인 브레이크포인트
```
Mobile:     ≤ 768px
Tablet:     768px - 1024px
Desktop:    ≥ 1024px
Large:      ≥ 1200px
```

---

## 📱 주요 페이지

### 1. 홈페이지 (index.html)
- 회사 소개
- 주요 서비스 안내
- 최신 뉴스

### 2. 회사소개 (company.html)
- 회사 정보
- 히스토리 타임라인
- CI/로고
- 연락처

### 3. 사업소개 (business.html)
- 서비스 분야 설명
- 프로세스
- 사례

### 4. 포트폴리오 (work.html)
- 포트폴리오 갤러리
- 프로젝트 상세

### 5. 뉴스룸 (newsroom.html)
- 보도자료
- 뉴스 아카이브

### 6. 연락처 (contact.html)
- 문의 폼
- 위치 정보
- 소셜 미디어

---

## 🚀 개발 가이드

### 문서 참조
- **POLICY.md**: 코딩 규칙 및 정책
- **DEVELOPMENT.md**: 개발 로드맵 및 계획

### 시작하기

1. 저장소 클론
```bash
git clone https://github.com/devkingKR/january-corporation.git
cd january-corporation
```

2. 로컬 서버 실행
```bash
# Python 3 사용 (간단한 HTTP 서버)
python3 -m http.server 8000
```

3. 브라우저에서 확인
```
http://localhost:8000
```

### CSS 수정

페이지별 CSS 파일로 분리되어 있습니다:
- `css/company-custom.css` - company.html
- `css/index-custom.css` - index.html
- 기타 `css/*-custom.css`

**중요**: HTML에 인라인 스타일 추가 금지

### 커밋 방식

```bash
git add .
git commit -m "카테고리: 변경 내용"
```

예시:
```bash
git commit -m "스타일: company.html 타이포그래피 개선"
git commit -m "기능: newsroom에 FAQ 섹션 추가"
```

---

## ✨ 최근 개선사항

### 2026년 4월
- ✅ 모든 페이지 인라인 CSS 외부화
- ✅ jQuery Migrate 제거
- ✅ 파일 크기 23% 감소
- ✅ 미완료 다운로드 파일 정리

---

## 📊 성능 지표

| 메트릭 | 값 |
|--------|-----|
| 전체 크기 | 378KB |
| company.html | 29KB |
| index.html | 121KB |
| 평균 페이지 | ~60KB |

**목표**: 페이지당 50KB 이하

---

## 🔗 링크

- [홈페이지](https://januarycorporation.com)
- [GitHub](https://github.com/devkingKR/january-corporation)
- [KakaoTalk](http://pf.kakao.com/_ZuStxb/chat)
- [YouTube](https://www.youtube.com/@january-corporation)
- [TikTok](https://www.tiktok.com/@january_corporation)

---

## 📝 라이선스

© January Corporation. All Rights Reserved.

---

더 질문이 있으시면 [연락처](./contact.html)에서 문의해주세요.
