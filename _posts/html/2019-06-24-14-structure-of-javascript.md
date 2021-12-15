---
title: "14_JAVA SCRIPT의 구조"
excerpt: "JAVA SCRIPT의 구조 학습 후 정리"
category: 
  - html
author_profile: true
sidebar:
  - nav: "main" 
---
<h4>
<pre>
JAVA SCRIPT 선언문
- &lt;script type="text/javascript"&gt;코드&lt;/script&gt;
- Head에 작성: script 코드를 브라우저가 해석하는 과정에서
              웹 사이트가 사용자에게 보여지는 전체적인 속도 저하
              script 코드가 먼저 동작해야 하는 경우에 작성
- Body에 작성: Html 코드를 우선 해석하고 사용자에게 보여준 후
              사용자 동작에 대한 반응이 이루어질 수 있도록 
              코드를 작성
              속도 향상을 위해 사용
- JavaScript 코드를 js라는 폴더에 외부 파일로 저장하고 불러오기 가능<br>
JAVA SCRIPT 동작
- DOM(Document Object Model) 구조
  : 하나의 문서는 하나의 객체로 다뤄질 수 있음
- HTML 파싱: HTML 확장자를 갖는 파일이 브라우저에서
            우리가 원하는 형태로 보일 수 있도록
            보내주는/불러오는 것
- 브라우저에서 작성한 코드가 보이는 과정
  : HTML 코드를 불러와서 DOM tree 분석
  → 렌더링하여 실제 페이지 만듦
  → 스타일 코드의 스타일을 적용
  → 재배치
  → 출력
