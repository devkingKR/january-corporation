# 문의 폼 기능 설계

**날짜**: 2026-04-07  
**대상 파일**: contact.html, privacy.html, css/contact-custom.css  
**배포 환경**: GitHub Pages (정적 HTML, 백엔드 없음)

---

## 1. 개요

January Corporation 공식 웹사이트 contact.html 페이지에 방문자가 직접 문의를 제출하면 운영자 이메일로 내용이 전달되는 문의 폼을 추가한다.

---

## 2. 이메일 전송 서비스

- **서비스**: [Formspree](https://formspree.io)
- **플랜**: 무료 (월 50건, 매월 1일 자동 리셋)
- **수신 이메일**: january.corporation2024@gmail.com
- **스팸 방지**: Formspree 기본 필터 내장
- **설정**: Formspree 가입 후 폼 엔드포인트 ID 발급 (`https://formspree.io/f/{ID}`)

월 50건은 충분하며, 초과 시 해당 월 나머지 기간 동안 제출이 차단되고 다음 달 자동 복구된다.

---

## 3. 신규/수정 파일

| 파일 | 작업 유형 | 내용 |
|------|-----------|------|
| `contact.html` | 수정 | 문의 폼 섹션 추가 |
| `privacy.html` | 신규 | 개인정보처리방침 페이지 |
| `css/contact-custom.css` | 수정 | 폼 및 개인정보 동의 체크박스 스타일 추가 |

---

## 4. 문의 폼 설계

### 4-1. 위치
contact.html 내 Google Maps 섹션(`.elementor-widget-google_maps`) 바로 아래에 새 `<section>` 추가.

### 4-2. 레이아웃
- **배경**: 사이트 그라디언트 (`linear-gradient(135deg, #667eea, #764ba2)`)
- **폼 카드**: 흰 배경(`#ffffff`), `border-radius: 12px`, `box-shadow` 적용
- **전체 너비**: 풀 와이드 섹션, 내부 최대 너비 `680px` 중앙 정렬
- **반응형**: 이름/이메일 2열 배치는 모바일에서 1열로 전환 (미디어 쿼리 1개)

### 4-3. 폼 필드

| 필드 | 타입 | 필수 | 비고 |
|------|------|------|------|
| 이름 | `<input type="text">` | ✅ | 이메일과 2열 배치 |
| 이메일 | `<input type="email">` | ✅ | 이름과 2열 배치 |
| 문의 유형 | `<select>` | ✅ | 광고 / 협업 / 기타 |
| 제목 | `<input type="text">` | ✅ | |
| 본문 | `<textarea>` | ✅ | 최소 높이 120px |
| 개인정보 동의 | `<input type="checkbox">` | ✅ | 미동의 시 전송 불가 |

### 4-4. 개인정보 동의 체크박스
```
☐ 개인정보 수집·이용에 동의합니다. [자세히 보기 →]
```
- `[자세히 보기]`는 `privacy.html`을 새 탭(`target="_blank"`)으로 열기
- 체크박스 미체크 시 HTML5 `required` 속성으로 브라우저 기본 검증 처리 (JS 불필요)

### 4-5. 전송 버튼
- 문구: **"문의 보내기"**
- 스타일: 그라디언트 버튼 (`#667eea` → `#764ba2`), 전체 너비

### 4-6. 전송 결과 처리
- **성공**: Formspree 리다이렉트 대신 JS로 성공 메시지 인라인 표시
  - 메시지: "문의가 접수되었습니다. 빠른 시일 내에 답변드리겠습니다."
- **실패**: "전송 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요."

---

## 5. 개인정보처리방침 페이지 (privacy.html)

### 5-1. 구조
기존 페이지(index.html 등)와 동일한 헤더·푸터 구조 사용.

### 5-2. 필수 기재 내용

| 항목 | 내용 |
|------|------|
| 수집 항목 | 이름, 이메일 주소 |
| 수집 목적 | 문의 접수 및 답변 |
| 보유 기간 | 문의 처리 완료 후 즉시 파기 |
| 제3자 제공 | 없음 (단, Formspree 서버를 경유하여 전송됨) |
| 이용자 권리 | 개인정보 열람·삭제 요청 가능 (이메일 문의) |
| 담당자 연락처 | january.corporation2024@gmail.com |

---

## 6. 구현 순서

1. Formspree 가입 → 새 폼 생성 → 엔드포인트 ID 확보
2. `privacy.html` 신규 작성
3. `contact.html`에 폼 섹션 HTML 추가
4. `css/contact-custom.css`에 폼 스타일 추가
5. JS로 폼 제출·성공/실패 메시지 처리
6. `python3 test_harness.py` 실행 및 브라우저 확인
7. 커밋 & 푸시

---

## 7. 제약사항

- HTML에 인라인 스타일(`style=""`) 추가 금지 (CLAUDE.md 규칙)
- CSS는 `css/contact-custom.css`에만 작성
- 메뉴 구조 변경 없음
- jQuery는 기존 `wp-includes/js/jquery/jquery.min.js` 사용 (추가 라이브러리 없음)
