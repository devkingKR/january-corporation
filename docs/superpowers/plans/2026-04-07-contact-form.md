# 문의 폼 기능 구현 계획

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** contact.html에 Formspree 기반 문의 폼을 추가하고, 개인정보처리방침 페이지(privacy.html)를 신규 작성한다.

**Architecture:** 정적 HTML 사이트이므로 백엔드 없이 Formspree API로 이메일 전송을 처리한다. 폼 HTML은 contact.html의 Google Maps 섹션 바로 아래에 삽입하고, 스타일은 css/contact-custom.css에만 추가한다. 폼 제출은 fetch()로 AJAX 처리해 페이지 이동 없이 성공/실패 메시지를 표시한다.

**Tech Stack:** HTML5, CSS3 (contact-custom.css), vanilla JS fetch API, Formspree (외부 이메일 전송 서비스)

---

## 파일 구조

| 파일 | 작업 | 변경 내용 |
|------|------|-----------|
| `contact.html` | 수정 | 폼 섹션 HTML 삽입 (line 363 이후), JS 스크립트 추가 (</body> 직전) |
| `privacy.html` | 신규 생성 | 개인정보처리방침 페이지 |
| `css/contact-custom.css` | 수정 | 폼 스타일 클래스 추가 |

---

## ⚠️ Task 0: [수동 작업] Formspree 폼 ID 발급

> **이 작업은 Claude가 아닌 사용자가 직접 수행해야 합니다.**

- [ ] **Step 1: Formspree 가입**

  브라우저에서 https://formspree.io 접속 → Sign Up → 이메일(january.corporation2024@gmail.com)로 가입

- [ ] **Step 2: 새 폼 생성**

  대시보드 → "New Form" 클릭 → 이름: "January Corporation 문의" → 이메일: january.corporation2024@gmail.com 입력 → Create

- [ ] **Step 3: 폼 ID 확인**

  생성된 폼의 엔드포인트 URL 복사:
  ```
  https://formspree.io/f/XXXXXXXX
  ```
  `XXXXXXXX` 부분이 폼 ID. Task 3에서 사용.

- [ ] **Step 4: 이메일 인증**

  Formspree가 발송한 인증 메일 확인 → "Confirm email" 클릭 (미인증 시 폼 제출이 차단됨)

---

## Task 1: privacy.html 신규 작성

**Files:**
- Create: `privacy.html`

- [ ] **Step 1: privacy.html 파일 생성**

  아래 내용 그대로 `privacy.html` 파일을 프로젝트 루트에 생성:

  ```html
  <!DOCTYPE html>
  <html class="html" lang="ko-KR">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>개인정보처리방침 – 제뉴어리코퍼레이션(주)</title>
    <meta name="robots" content="noindex">

    <link rel="stylesheet" id="wp-block-library-css" href="./contact/style.min.css" media="all">
    <link rel='stylesheet' id='font-awesome-css' href='css/fontawesome-all.min.css' media='all'/>
    <link rel='stylesheet' id='simple-line-icons-css' href='css/simple-line-icons.min.css' media='all'/>
    <link rel='stylesheet' id='oceanwp-style-css' href='css/oceanwp-style.css' media='all'/>
    <link rel='stylesheet' id='elementor-frontend-css' href='css/frontend.min.css' media='all'/>
    <link rel='stylesheet' id='elementor-global-css' href='css/global.css' media='all'/>
    <link rel='stylesheet' id='contact-custom-css' href='css/contact-custom.css' media='all'/>
    <link rel='stylesheet' id='google-fonts-1-css' href='https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700;800&family=Noto+Sans+KR:wght@300;400;500;600;700&display=swap' media='all'/>
    <link rel='stylesheet' id='elementor-icons-shared-0-css' href='css/fontawesome.min.css' media='all'/>
    <link rel='stylesheet' id='elementor-icons-fa-solid-css' href='css/solid.min.css' media='all'/>

    <script src="./wp-includes/js/jquery/jquery.min.js" id="jquery-core-js"></script>

    <link rel="icon" href="./wp-content/uploads/2025/12/cropped-cropped-%EC%A0%9C%EB%89%B4%EC%96%B4%EB%A6%AC-%EB%A1%9C%EA%B3%A0-ci-091441559-1-32x32.jpg" sizes="32x32">
    <link rel="icon" href="./wp-content/uploads/2025/12/cropped-cropped-%EC%A0%9C%EB%89%B4%EC%96%B4%EB%A6%AC-%EB%A1%9C%EA%B3%A0-ci-091441559-1-192x192.jpg" sizes="192x192">
    <link rel="apple-touch-icon" href="./wp-content/uploads/2025/12/cropped-cropped-%EC%A0%9C%EB%89%B4%EC%96%B4%EB%A6%AC-%EB%A1%9C%EA%B3%A0-ci-091441559-1-180x180.jpg">
  </head>

  <body class="wp-singular page-template-default page wp-custom-logo wp-embed-responsive wp-theme-oceanwp oceanwp-theme content-full-screen page-header-disabled" itemscope itemtype="https://schema.org/WebPage">

  <div id="outer-wrap" class="site clr">
  <div id="wrap" class="clr">

    <header id="site-header" class="full_screen-header clr" data-height="70" itemscope itemtype="https://schema.org/WPHeader" role="banner">
      <div id="site-header-inner" class="clr container">
        <div id="site-logo" class="clr" itemscope itemtype="https://schema.org/Brand">
          <div id="site-logo-inner" class="clr">
            <a href="./index.html" class="custom-logo-link" rel="home">
              <img width="262" height="194" src="./wp-content/uploads/2024/01/cropped-제뉴어리-코퍼레이션-1.jpg" class="custom-logo" alt="제뉴어리코퍼레이션(주)" decoding="async" fetchpriority="high" srcset="./wp-content/uploads/2024/01/cropped-제뉴어리-코퍼레이션-1.jpg 1x, ./wp-content/uploads/2025/09/04_january-corp_CI_세로_어두운배경.png 2x"/>
            </a>
          </div>
        </div>
        <div id="site-navigation-wrap" class="clr">
          <div class="menu-bar-wrap clr">
            <div class="menu-bar-inner clr">
              <a href="#header-menu-toggle" class="menu-bar">
                <span class="ham"></span>
                <span class="screen-reader-text">View website Menu</span>
              </a>
            </div>
          </div>
          <div id="full-screen-menu" class="clr">
            <div id="full-screen-menu-inner" class="clr">
              <nav id="site-navigation" class="navigation main-navigation clr" itemscope itemtype="https://schema.org/SiteNavigationElement" role="navigation">
                <ul id="menu-test_top-bar" class="main-menu fs-dropdown-menu">
                  <li class="menu-item"><a href="./newsroom.html" class="menu-link"><span class="text-wrap">NEWSROOM</span></a></li>
                  <li class="menu-item"><a href="./work.html" class="menu-link"><span class="text-wrap">Work</span></a></li>
                  <li class="menu-item"><a href="./contact.html" class="menu-link"><span class="text-wrap">CONTACT</span></a></li>
                  <li class="menu-item"><a href="./business.html" class="menu-link"><span class="text-wrap">BUSINESS</span></a></li>
                  <li class="menu-item"><a href="./company.html" class="menu-link"><span class="text-wrap">COMPANY</span></a></li>
                </ul>
              </nav>
            </div>
          </div>
        </div>
        <div class="mobile-menu-toggle" id="mobile-menu-toggle" aria-label="메뉴 열기/닫기">
          <span></span><span></span><span></span>
        </div>
        <div class="oceanwp-mobile-menu-icon clr mobile-right">
          <a href="#mobile-menu-toggle" class="mobile-menu" aria-label="Mobile Menu">
            <i class="fa fa-bars" aria-hidden="true"></i>
            <span class="oceanwp-text">Menu</span>
            <span class="oceanwp-close-text">Close</span>
          </a>
        </div>
      </div>
      <div id="mobile-dropdown" class="clr">
        <nav class="clr" itemscope itemtype="https://schema.org/SiteNavigationElement">
          <div id="mobile-nav" class="navigation clr">
            <ul id="menu-test_top-bar-1" class="menu">
              <li class="menu-item"><a href="./newsroom.html">NEWSROOM</a></li>
              <li class="menu-item"><a href="./work.html">Work</a></li>
              <li class="menu-item"><a href="./contact.html">CONTACT</a></li>
              <li class="menu-item"><a href="./business.html">BUSINESS</a></li>
              <li class="menu-item"><a href="./company.html">COMPANY</a></li>
            </ul>
          </div>
        </nav>
      </div>
    </header>

    <main id="main" class="site-main clr" role="main">
      <div id="content-wrap" class="container clr">
        <div id="primary" class="content-area clr">
          <div id="content" class="site-content clr">
            <article class="single-page-article clr">
              <div class="entry clr" itemprop="text">

                <section class="privacy-section">
                  <div class="privacy-inner">
                    <h1 class="privacy-title">개인정보처리방침</h1>
                    <p class="privacy-updated">최종 수정일: 2026년 4월 7일</p>

                    <div class="privacy-block">
                      <h2 class="privacy-heading">1. 수집하는 개인정보 항목</h2>
                      <p>제뉴어리코퍼레이션(주)(이하 "회사")는 문의 접수를 위해 아래 정보를 수집합니다.</p>
                      <ul>
                        <li>이름</li>
                        <li>이메일 주소</li>
                        <li>문의 유형, 제목, 문의 내용 (이용자 작성 정보)</li>
                      </ul>
                    </div>

                    <div class="privacy-block">
                      <h2 class="privacy-heading">2. 개인정보의 수집 및 이용 목적</h2>
                      <p>수집된 개인정보는 <strong>문의 접수 및 답변 제공</strong> 목적으로만 사용됩니다. 이외의 목적으로 사용하지 않습니다.</p>
                    </div>

                    <div class="privacy-block">
                      <h2 class="privacy-heading">3. 개인정보의 보유 및 이용 기간</h2>
                      <p>문의 처리 완료 후 즉시 파기합니다. 단, 관계 법령에 의해 보존이 필요한 경우 해당 법령이 정한 기간 동안 보관합니다.</p>
                    </div>

                    <div class="privacy-block">
                      <h2 class="privacy-heading">4. 개인정보의 제3자 제공</h2>
                      <p>회사는 이용자의 개인정보를 원칙적으로 제3자에게 제공하지 않습니다. 단, 문의 폼 제출 시 이메일 전송 서비스인 <strong>Formspree</strong>(formspree.io)의 서버를 경유하여 전송됩니다. Formspree의 개인정보 처리방침은 <a href="https://formspree.io/legal/privacy-policy" target="_blank" rel="noopener">Formspree 사이트</a>에서 확인하실 수 있습니다.</p>
                    </div>

                    <div class="privacy-block">
                      <h2 class="privacy-heading">5. 이용자의 권리</h2>
                      <p>이용자는 언제든지 자신의 개인정보에 대한 열람, 수정, 삭제를 요청할 수 있습니다. 아래 이메일로 문의해주세요.</p>
                    </div>

                    <div class="privacy-block">
                      <h2 class="privacy-heading">6. 개인정보 보호 담당자</h2>
                      <ul>
                        <li>회사명: 제뉴어리코퍼레이션(주)</li>
                        <li>이메일: january.corporation2024@gmail.com</li>
                      </ul>
                    </div>

                    <div class="privacy-back">
                      <a href="./contact.html" class="privacy-back-link">← 문의하기 페이지로 돌아가기</a>
                    </div>
                  </div>
                </section>

              </div>
            </article>
          </div>
        </div>
      </div>
    </main>

  </div>
  </div>

  <script src="./wp-content/themes/oceanwp/assets/js/theme.min.js" id="oceanwp-main-js"></script>
  <script src="./wp-content/themes/oceanwp/assets/js/drop-down-mobile-menu.min.js" id="oceanwp-drop-down-mobile-menu-js"></script>

  </body>
  </html>
  ```

- [ ] **Step 2: 로컬에서 파일 열어 확인**

  브라우저에서 `http://localhost:8000/privacy.html` 접속해 헤더 메뉴와 개인정보 내용이 정상 표시되는지 확인.  
  (로컬 서버가 없으면: `python3 -m http.server 8000`)

- [ ] **Step 3: 커밋**

  ```bash
  git add privacy.html
  git commit -m "기능: 개인정보처리방침 페이지(privacy.html) 추가"
  ```

---

## Task 2: css/contact-custom.css 폼 스타일 추가

**Files:**
- Modify: `css/contact-custom.css`

- [ ] **Step 1: css/contact-custom.css 파일 맨 끝에 아래 CSS 추가**

  ```css
  /* ===== 문의 폼 섹션 ===== */
  .contact-form-section {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      padding: 60px 20px;
      width: 100%;
      box-sizing: border-box;
  }

  .contact-form-inner {
      max-width: 680px;
      margin: 0 auto;
  }

  .contact-form-header {
      text-align: center;
      margin-bottom: 32px;
  }

  .contact-form-divider {
      width: 28px;
      height: 4px;
      background: rgba(255, 255, 255, 0.5);
      margin: 0 auto 16px;
      border-radius: 2px;
  }

  .contact-form-title {
      color: #ffffff;
      font-size: 24px;
      font-weight: 700;
      margin: 0 0 8px;
  }

  .contact-form-subtitle {
      color: rgba(255, 255, 255, 0.8);
      font-size: 14px;
      margin: 0;
  }

  .contact-form-card {
      background: #ffffff;
      border-radius: 12px;
      padding: 36px;
      box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
  }

  .contact-form-row {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 16px;
      margin-bottom: 16px;
  }

  .contact-form-group {
      margin-bottom: 16px;
  }

  .contact-form-group label {
      display: block;
      font-size: 13px;
      font-weight: 600;
      color: #333333;
      margin-bottom: 6px;
  }

  .contact-required {
      color: #667eea;
  }

  .contact-form-group input[type="text"],
  .contact-form-group input[type="email"],
  .contact-form-group select,
  .contact-form-group textarea {
      width: 100%;
      border: 1.5px solid #e0e0e0;
      border-radius: 8px;
      padding: 10px 14px;
      font-size: 14px;
      color: #333333;
      background: #fafafa;
      box-sizing: border-box;
      font-family: 'Noto Sans KR', sans-serif;
      transition: border-color 0.2s;
  }

  .contact-form-group input[type="text"]:focus,
  .contact-form-group input[type="email"]:focus,
  .contact-form-group select:focus,
  .contact-form-group textarea:focus {
      outline: none;
      border-color: #667eea;
      background: #ffffff;
  }

  .contact-form-group textarea {
      min-height: 120px;
      resize: vertical;
  }

  .contact-form-privacy {
      margin-bottom: 20px;
  }

  .contact-privacy-label {
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 13px;
      color: #555555;
      cursor: pointer;
  }

  .contact-privacy-label input[type="checkbox"] {
      width: 16px;
      height: 16px;
      accent-color: #667eea;
      cursor: pointer;
      flex-shrink: 0;
  }

  .contact-privacy-link {
      color: #667eea;
      text-decoration: underline;
      white-space: nowrap;
  }

  .contact-form-submit {
      width: 100%;
      background: linear-gradient(135deg, #667eea, #764ba2);
      color: #ffffff;
      border: none;
      border-radius: 8px;
      padding: 14px;
      font-size: 16px;
      font-weight: 700;
      cursor: pointer;
      font-family: 'Noto Sans KR', sans-serif;
      letter-spacing: 0.5px;
      transition: opacity 0.2s;
  }

  .contact-form-submit:hover {
      opacity: 0.9;
  }

  .contact-form-notice {
      text-align: center;
      font-size: 12px;
      color: #aaaaaa;
      margin: 12px 0 0;
  }

  .contact-form-hidden {
      display: none;
  }

  .contact-form-success {
      text-align: center;
      padding: 32px 24px;
      color: #667eea;
      font-size: 16px;
      font-weight: 600;
      line-height: 1.6;
  }

  .contact-form-error {
      text-align: center;
      padding: 16px;
      color: #e53e3e;
      font-size: 14px;
      margin-top: 12px;
  }

  /* ===== 개인정보처리방침 페이지 ===== */
  .privacy-section {
      padding: 60px 20px;
      background: #ffffff;
  }

  .privacy-inner {
      max-width: 720px;
      margin: 0 auto;
  }

  .privacy-title {
      font-size: 28px;
      font-weight: 700;
      color: #000000;
      margin: 0 0 8px;
  }

  .privacy-updated {
      font-size: 13px;
      color: #999999;
      margin: 0 0 40px;
  }

  .privacy-block {
      margin-bottom: 32px;
  }

  .privacy-heading {
      font-size: 16px;
      font-weight: 700;
      color: #333333;
      margin: 0 0 10px;
      padding-bottom: 8px;
      border-bottom: 1px solid #eeeeee;
  }

  .privacy-block p,
  .privacy-block ul {
      font-size: 14px;
      color: #555555;
      line-height: 1.8;
      margin: 0;
  }

  .privacy-block ul {
      padding-left: 20px;
  }

  .privacy-block a {
      color: #667eea;
      text-decoration: underline;
  }

  .privacy-back {
      margin-top: 40px;
      padding-top: 24px;
      border-top: 1px solid #eeeeee;
  }

  .privacy-back-link {
      font-size: 14px;
      color: #667eea;
      text-decoration: none;
  }

  .privacy-back-link:hover {
      text-decoration: underline;
  }

  /* ===== 반응형 ===== */
  @media (max-width: 600px) {
      .contact-form-row {
          grid-template-columns: 1fr;
      }
      .contact-form-card {
          padding: 24px 16px;
      }
      .contact-form-section {
          padding: 40px 16px;
      }
  }
  ```

- [ ] **Step 2: 커밋**

  ```bash
  git add css/contact-custom.css
  git commit -m "스타일: 문의 폼 및 개인정보처리방침 CSS 추가"
  ```

---

## Task 3: contact.html 폼 HTML 삽입

**Files:**
- Modify: `contact.html`

> **전제조건**: Task 0에서 발급받은 Formspree 폼 ID가 있어야 합니다. (`XXXXXXXX` 자리에 실제 ID 입력)

- [ ] **Step 1: 삽입 위치 확인**

  contact.html에서 아래 문자열을 찾는다 (line ~364):
  ```
  elementor-element-286c02b6 envato-kit-141-top-0
  ```
  이 `<section>` 태그 **바로 앞**에 폼 섹션을 삽입한다.

- [ ] **Step 2: 폼 HTML 삽입**

  위에서 찾은 `<section class="... elementor-element-286c02b6 ...">` 바로 앞에 아래 HTML을 삽입:

  ```html
  <!-- 문의 폼 섹션 -->
  <section class="contact-form-section">
      <div class="contact-form-inner">
          <div class="contact-form-header">
              <div class="contact-form-divider"></div>
              <h2 class="contact-form-title">문의하기</h2>
              <p class="contact-form-subtitle">궁금하신 점이 있으시면 아래 양식을 작성해 보내주세요.</p>
          </div>
          <div class="contact-form-card">
              <form id="contact-form" action="https://formspree.io/f/XXXXXXXX" method="POST">
                  <div class="contact-form-row">
                      <div class="contact-form-group">
                          <label for="contact-name">이름 <span class="contact-required">*</span></label>
                          <input type="text" id="contact-name" name="name" placeholder="홍길동" required>
                      </div>
                      <div class="contact-form-group">
                          <label for="contact-email">이메일 <span class="contact-required">*</span></label>
                          <input type="email" id="contact-email" name="email" placeholder="example@email.com" required>
                      </div>
                  </div>
                  <div class="contact-form-group">
                      <label for="contact-type">문의 유형 <span class="contact-required">*</span></label>
                      <select id="contact-type" name="inquiry_type" required>
                          <option value="" disabled selected>선택해주세요</option>
                          <option value="광고">광고</option>
                          <option value="협업">협업</option>
                          <option value="기타">기타</option>
                      </select>
                  </div>
                  <div class="contact-form-group">
                      <label for="contact-subject">제목 <span class="contact-required">*</span></label>
                      <input type="text" id="contact-subject" name="subject" placeholder="문의 제목을 입력해주세요" required>
                  </div>
                  <div class="contact-form-group">
                      <label for="contact-message">문의 내용 <span class="contact-required">*</span></label>
                      <textarea id="contact-message" name="message" placeholder="문의하실 내용을 자세히 작성해주세요." required></textarea>
                  </div>
                  <div class="contact-form-privacy">
                      <label class="contact-privacy-label">
                          <input type="checkbox" name="privacy_agree" required>
                          개인정보 수집·이용에 동의합니다.
                          <a href="./privacy.html" target="_blank" class="contact-privacy-link">자세히 보기 →</a>
                      </label>
                  </div>
                  <button type="submit" class="contact-form-submit">문의 보내기</button>
                  <p class="contact-form-notice">* 입력하신 정보는 문의 답변 목적으로만 사용됩니다.</p>
              </form>
              <div id="contact-form-success" class="contact-form-success contact-form-hidden">
                  문의가 접수되었습니다.<br>빠른 시일 내에 답변드리겠습니다.
              </div>
              <div id="contact-form-error" class="contact-form-error contact-form-hidden">
                  전송 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요.
              </div>
          </div>
      </div>
  </section>
  ```

- [ ] **Step 3: 브라우저에서 폼 표시 확인**

  `http://localhost:8000/contact.html` 접속 → 지도 아래에 그라디언트 배경 폼이 표시되는지 확인.  
  필드 5개, 동의 체크박스, 전송 버튼이 모두 보여야 함.

- [ ] **Step 4: 커밋**

  ```bash
  git add contact.html
  git commit -m "기능: contact.html에 문의 폼 섹션 HTML 추가"
  ```

---

## Task 4: contact.html JS 폼 제출 처리 추가

**Files:**
- Modify: `contact.html` (</body> 직전 `<script>` 태그 추가)

- [ ] **Step 1: contact.html 맨 아래 `</body>` 바로 위에 JS 추가**

  contact.html의 `</body>` 태그를 찾아 그 바로 위에 아래 스크립트 삽입:

  ```html
  <script>
  (function () {
      var form = document.getElementById('contact-form');
      if (!form) return;

      form.addEventListener('submit', function (e) {
          e.preventDefault();

          var submitBtn = form.querySelector('.contact-form-submit');
          var successEl = document.getElementById('contact-form-success');
          var errorEl = document.getElementById('contact-form-error');

          submitBtn.disabled = true;
          submitBtn.textContent = '전송 중...';
          errorEl.classList.add('contact-form-hidden');

          fetch(form.action, {
              method: 'POST',
              body: new FormData(form),
              headers: { 'Accept': 'application/json' }
          })
          .then(function (response) {
              if (response.ok) {
                  form.classList.add('contact-form-hidden');
                  successEl.classList.remove('contact-form-hidden');
              } else {
                  errorEl.classList.remove('contact-form-hidden');
                  submitBtn.disabled = false;
                  submitBtn.textContent = '문의 보내기';
              }
          })
          .catch(function () {
              errorEl.classList.remove('contact-form-hidden');
              submitBtn.disabled = false;
              submitBtn.textContent = '문의 보내기';
          });
      });
  }());
  </script>
  ```

- [ ] **Step 2: 필수 필드 미입력 시 브라우저 검증 확인**

  `http://localhost:8000/contact.html` → 폼을 비워두고 "문의 보내기" 클릭 → 브라우저 기본 required 검증 메시지가 뜨는지 확인.

- [ ] **Step 3: 개인정보 동의 미체크 시 차단 확인**

  모든 필드를 채우고 동의 체크박스만 체크하지 않은 채 전송 → 체크박스 required 검증으로 차단되는지 확인.

- [ ] **Step 4: 커밋**

  ```bash
  git add contact.html
  git commit -m "기능: 문의 폼 AJAX 제출 및 성공/실패 메시지 처리 JS 추가"
  ```

---

## Task 5: 전체 테스트 및 최종 커밋

**Files:** 없음 (테스트만)

- [ ] **Step 1: test_harness.py 실행**

  ```bash
  python3 test_harness.py
  ```
  Expected: 모든 테스트 PASS

- [ ] **Step 2: 모바일 반응형 확인**

  브라우저 개발자 도구(F12) → 모바일 뷰(375px) → 이름/이메일 필드가 1열로 쌓이는지 확인.

- [ ] **Step 3: [Formspree ID 입력된 경우] 실제 제출 테스트**

  실제로 폼을 작성하고 전송 → january.corporation2024@gmail.com 수신함에서 이메일 도착 확인 → 성공 메시지 표시 확인.

- [ ] **Step 4: 최종 커밋 및 푸시**

  ```bash
  git add .
  git commit -m "기능: 문의 폼 및 개인정보처리방침 페이지 구현 완료"
  git push
  ```
  푸시 후 https://januarycorporation.com/contact.html 에서 실제 배포 확인.
