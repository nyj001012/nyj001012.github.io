---
title: "회원 관리 예제"
excerpt: "회원 관리 서비스 개발 및 테스트 예제"
category: 
  - springboot
author_profile: true
sidebar:
  - nav: "main" 
tag:
  - spring boot
  - thymeleaf
toc: true
toc_sticky: true
last_modified_at: 2024-03-21T00:00:00+09:00
---

> 이 포스트는 김영한님의 ['스프링 입문 - 코드로 배우는 스프링 부트, 웹 MVC, DB 접근 기술'](https://www.inflearn.com/course/%EC%8A%A4%ED%94%84%EB%A7%81-%EC%9E%85%EB%AC%B8-%EC%8A%A4%ED%94%84%EB%A7%81%EB%B6%80%ED%8A%B8/dashboard)을 수강하고 작성하였습니다.  

# 일반적인 웹 어플리케이션 계층 구조
<svg version="1.1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 729.5244448751397 303.5878809224305" width="729.5244448751397" height="303.5878809224305">
  <!-- svg-source:excalidraw -->
  
  <defs>
    <style class="style-fonts">
      @font-face {
        font-family: "Virgil";
        src: url("https://excalidraw.com/Virgil.woff2");
      }
      @font-face {
        font-family: "Cascadia";
        src: url("https://excalidraw.com/Cascadia.woff2");
      }
      @font-face {
        font-family: "Assistant";
        src: url("https://excalidraw.com/Assistant-Regular.woff2");
      }
    </style>
    
  </defs>
  <rect x="0" y="0" width="729.5244448751397" height="303.5878809224305" fill="#ffffff"></rect><g stroke-linecap="round" transform="translate(10 20.87542036839568) rotate(0 75.98331674657287 39.668400582715435)"><path d="M0 0 C33.59 0, 67.17 0, 151.97 0 M0 0 C31.69 0, 63.39 0, 151.97 0 M151.97 0 C151.97 17.16, 151.97 34.33, 151.97 79.34 M151.97 0 C151.97 17.93, 151.97 35.87, 151.97 79.34 M151.97 79.34 C98.72 79.34, 45.47 79.34, 0 79.34 M151.97 79.34 C110.3 79.34, 68.64 79.34, 0 79.34 M0 79.34 C0 62.24, 0 45.15, 0 0 M0 79.34 C0 58.71, 0 38.08, 0 0" stroke="#1e1e1e" stroke-width="2" fill="none"></path></g><g transform="translate(58.30332407079163 51.343820951111184) rotate(0 27.67999267578125 9.200000000000045)"><text x="27.67999267578125" y="0" font-family="Helvetica, Segoe UI Emoji" font-size="16px" fill="#1e1e1e" text-anchor="middle" style="white-space: pre;" direction="ltr" dominant-baseline="text-before-edge">컨트롤러</text></g><g stroke-linecap="round" transform="translate(214.8991058444269 21.746745722643027) rotate(0 75.98331674657287 39.668400582715435)"><path d="M0 0 C59.69 0, 119.38 0, 151.97 0 M0 0 C50.83 0, 101.66 0, 151.97 0 M151.97 0 C151.97 20.49, 151.97 40.99, 151.97 79.34 M151.97 0 C151.97 28.02, 151.97 56.03, 151.97 79.34 M151.97 79.34 C99.93 79.34, 47.88 79.34, 0 79.34 M151.97 79.34 C109.7 79.34, 67.44 79.34, 0 79.34 M0 79.34 C0 54.57, 0 29.79, 0 0 M0 79.34 C0 48, 0 16.67, 0 0" stroke="#1e1e1e" stroke-width="2" fill="none"></path></g><g transform="translate(270.12242808416386 52.21514630535853) rotate(0 20.759994506835938 9.200000000000045)"><text x="20.759994506835938" y="0" font-family="Helvetica, Segoe UI Emoji" font-size="16px" fill="#1e1e1e" text-anchor="middle" style="white-space: pre;" direction="ltr" dominant-baseline="text-before-edge">서비스</text></g><g stroke-linecap="round" transform="translate(422.38647721485614 21.20447038717066) rotate(0 75.98331674657288 39.668400582715435)"><path d="M0 0 C39.03 0, 78.07 0, 151.97 0 M0 0 C39.43 0, 78.86 0, 151.97 0 M151.97 0 C151.97 26.86, 151.97 53.72, 151.97 79.34 M151.97 0 C151.97 15.94, 151.97 31.88, 151.97 79.34 M151.97 79.34 C103.64 79.34, 55.31 79.34, 0 79.34 M151.97 79.34 C101.33 79.34, 50.69 79.34, 0 79.34 M0 79.34 C0 48.36, 0 17.38, 0 0 M0 79.34 C0 47.72, 0 16.11, 0 0" stroke="#1e1e1e" stroke-width="2" fill="none"></path></g><g transform="translate(463.76980311670246 51.67287096988616) rotate(0 34.59999084472656 9.200000000000045)"><text x="34.59999084472656" y="0" font-family="Helvetica, Segoe UI Emoji" font-size="16px" fill="#1e1e1e" text-anchor="middle" style="white-space: pre;" direction="ltr" dominant-baseline="text-before-edge">리포지토리</text></g><g stroke-linecap="round" transform="translate(214.13525090879318 163.56049232505484) rotate(0 75.98331674657287 39.668400582715435)"><path d="M0 0 C50.77 0, 101.54 0, 151.97 0 M0 0 C50.43 0, 100.85 0, 151.97 0 M151.97 0 C151.97 27.28, 151.97 54.57, 151.97 79.34 M151.97 0 C151.97 22.07, 151.97 44.15, 151.97 79.34 M151.97 79.34 C100.3 79.34, 48.64 79.34, 0 79.34 M151.97 79.34 C116.4 79.34, 80.84 79.34, 0 79.34 M0 79.34 C0 59.24, 0 39.14, 0 0 M0 79.34 C0 53.77, 0 28.2, 0 0" stroke="#1e1e1e" stroke-width="2" fill="none"></path></g><g transform="translate(269.3585731485301 194.02889290777034) rotate(0 20.759994506835938 9.200000000000045)"><text x="20.759994506835938" y="0" font-family="Helvetica, Segoe UI Emoji" font-size="16px" fill="#1e1e1e" text-anchor="middle" style="white-space: pre;" direction="ltr" dominant-baseline="text-before-edge">도메인</text></g><g stroke-linecap="round" transform="translate(636.6654400300881 90.66518134761736) rotate(0 41.288205391590736 12.109209034928313)"><path d="M82.58 12.11 C82.58 12.81, 82.36 13.52, 81.95 14.21 C81.53 14.9, 80.9 15.59, 80.09 16.25 C79.27 16.91, 78.24 17.56, 77.04 18.16 C75.85 18.77, 74.45 19.36, 72.92 19.89 C71.38 20.43, 69.66 20.93, 67.83 21.39 C66 21.84, 64 22.25, 61.93 22.6 C59.86 22.95, 57.66 23.25, 55.41 23.49 C53.16 23.73, 50.81 23.91, 48.46 24.03 C46.1 24.16, 43.68 24.22, 41.29 24.22 C38.9 24.22, 36.47 24.16, 34.12 24.03 C31.77 23.91, 29.41 23.73, 27.17 23.49 C24.92 23.25, 22.71 22.95, 20.64 22.6 C18.57 22.25, 16.58 21.84, 14.75 21.39 C12.92 20.93, 11.2 20.43, 9.66 19.89 C8.12 19.36, 6.73 18.77, 5.53 18.16 C4.34 17.56, 3.31 16.91, 2.49 16.25 C1.67 15.59, 1.04 14.9, 0.63 14.21 C0.21 13.52, 0 12.81, 0 12.11 C0 11.41, 0.21 10.7, 0.63 10.01 C1.04 9.32, 1.67 8.63, 2.49 7.97 C3.31 7.31, 4.34 6.66, 5.53 6.05 C6.73 5.45, 8.12 4.86, 9.66 4.33 C11.2 3.79, 12.92 3.28, 14.75 2.83 C16.58 2.38, 18.57 1.97, 20.64 1.62 C22.71 1.27, 24.92 0.97, 27.17 0.73 C29.41 0.49, 31.77 0.31, 34.12 0.18 C36.47 0.06, 38.9 0, 41.29 0 C43.68 0, 46.1 0.06, 48.46 0.18 C50.81 0.31, 53.16 0.49, 55.41 0.73 C57.66 0.97, 59.86 1.27, 61.93 1.62 C64 1.97, 66 2.38, 67.83 2.83 C69.66 3.28, 71.38 3.79, 72.92 4.33 C74.45 4.86, 75.85 5.45, 77.04 6.05 C78.24 6.66, 79.27 7.31, 80.09 7.97 C80.9 8.63, 81.53 9.32, 81.95 10.01 C82.36 10.7, 82.47 11.76, 82.58 12.11 C82.68 12.46, 82.68 11.76, 82.58 12.11" stroke="none" stroke-width="0" fill="#fff9db"></path><path d="M82.58 12.11 C82.58 12.81, 82.36 13.52, 81.95 14.21 C81.53 14.9, 80.9 15.59, 80.09 16.25 C79.27 16.91, 78.24 17.56, 77.04 18.16 C75.85 18.77, 74.45 19.36, 72.92 19.89 C71.38 20.43, 69.66 20.93, 67.83 21.39 C66 21.84, 64 22.25, 61.93 22.6 C59.86 22.95, 57.66 23.25, 55.41 23.49 C53.16 23.73, 50.81 23.91, 48.46 24.03 C46.1 24.16, 43.68 24.22, 41.29 24.22 C38.9 24.22, 36.47 24.16, 34.12 24.03 C31.77 23.91, 29.41 23.73, 27.17 23.49 C24.92 23.25, 22.71 22.95, 20.64 22.6 C18.57 22.25, 16.58 21.84, 14.75 21.39 C12.92 20.93, 11.2 20.43, 9.66 19.89 C8.12 19.36, 6.73 18.77, 5.53 18.16 C4.34 17.56, 3.31 16.91, 2.49 16.25 C1.67 15.59, 1.04 14.9, 0.63 14.21 C0.21 13.52, 0 12.81, 0 12.11 C0 11.41, 0.21 10.7, 0.63 10.01 C1.04 9.32, 1.67 8.63, 2.49 7.97 C3.31 7.31, 4.34 6.66, 5.53 6.05 C6.73 5.45, 8.12 4.86, 9.66 4.33 C11.2 3.79, 12.92 3.28, 14.75 2.83 C16.58 2.38, 18.57 1.97, 20.64 1.62 C22.71 1.27, 24.92 0.97, 27.17 0.73 C29.41 0.49, 31.77 0.31, 34.12 0.18 C36.47 0.06, 38.9 0, 41.29 0 C43.68 0, 46.1 0.06, 48.46 0.18 C50.81 0.31, 53.16 0.49, 55.41 0.73 C57.66 0.97, 59.86 1.27, 61.93 1.62 C64 1.97, 66 2.38, 67.83 2.83 C69.66 3.28, 71.38 3.79, 72.92 4.33 C74.45 4.86, 75.85 5.45, 77.04 6.05 C78.24 6.66, 79.27 7.31, 80.09 7.97 C80.9 8.63, 81.53 9.32, 81.95 10.01 C82.36 10.7, 82.47 11.76, 82.58 12.11 C82.68 12.46, 82.68 11.76, 82.58 12.11" stroke="#ffd43b" stroke-width="2" fill="none"></path></g><g stroke-linecap="round" transform="translate(636.7063074363248 22.408653251337455) rotate(0 41.350717619502774 40.15673964708333)"><path d="M0 0 L82.7 0 L82.7 80.31 L0 80.31" stroke="none" stroke-width="0" fill="#fff9db"></path><path d="M0 0 C20.71 0, 41.42 0, 82.7 0 M0 0 C18.09 0, 36.18 0, 82.7 0 M82.7 0 C82.7 16.3, 82.7 32.61, 82.7 80.31 M82.7 0 C82.7 31.01, 82.7 62.02, 82.7 80.31 M82.7 80.31 C61.79 80.31, 40.89 80.31, 0 80.31 M82.7 80.31 C63.18 80.31, 43.65 80.31, 0 80.31 M0 80.31 C0 58.98, 0 37.65, 0 0 M0 80.31 C0 56.16, 0 32.01, 0 0" stroke="transparent" stroke-width="2" fill="none"></path></g><g transform="translate(666.9437438058276 53.36539289842085) rotate(0 11.11328125 9.200000000000045)"><text x="11.11328125" y="0" font-family="Helvetica, Segoe UI Emoji" font-size="16px" fill="#1e1e1e" text-anchor="middle" style="white-space: pre;" direction="ltr" dominant-baseline="text-before-edge">DB</text></g><g stroke-linecap="round" transform="translate(636.9480340919582 10) rotate(0 41.288205391590736 12.109209034928313)"><path d="M82.58 12.11 C82.58 12.81, 82.36 13.52, 81.95 14.21 C81.53 14.9, 80.9 15.59, 80.09 16.25 C79.27 16.91, 78.24 17.56, 77.04 18.16 C75.85 18.77, 74.45 19.36, 72.92 19.89 C71.38 20.43, 69.66 20.93, 67.83 21.39 C66 21.84, 64 22.25, 61.93 22.6 C59.86 22.95, 57.66 23.25, 55.41 23.49 C53.16 23.73, 50.81 23.91, 48.46 24.03 C46.1 24.16, 43.68 24.22, 41.29 24.22 C38.9 24.22, 36.47 24.16, 34.12 24.03 C31.77 23.91, 29.41 23.73, 27.17 23.49 C24.92 23.25, 22.71 22.95, 20.64 22.6 C18.57 22.25, 16.58 21.84, 14.75 21.39 C12.92 20.93, 11.2 20.43, 9.66 19.89 C8.12 19.36, 6.73 18.77, 5.53 18.16 C4.34 17.56, 3.31 16.91, 2.49 16.25 C1.67 15.59, 1.04 14.9, 0.63 14.21 C0.21 13.52, 0 12.81, 0 12.11 C0 11.41, 0.21 10.7, 0.63 10.01 C1.04 9.32, 1.67 8.63, 2.49 7.97 C3.31 7.31, 4.34 6.66, 5.53 6.05 C6.73 5.45, 8.12 4.86, 9.66 4.33 C11.2 3.79, 12.92 3.28, 14.75 2.83 C16.58 2.38, 18.57 1.97, 20.64 1.62 C22.71 1.27, 24.92 0.97, 27.17 0.73 C29.41 0.49, 31.77 0.31, 34.12 0.18 C36.47 0.06, 38.9 0, 41.29 0 C43.68 0, 46.1 0.06, 48.46 0.18 C50.81 0.31, 53.16 0.49, 55.41 0.73 C57.66 0.97, 59.86 1.27, 61.93 1.62 C64 1.97, 66 2.38, 67.83 2.83 C69.66 3.28, 71.38 3.79, 72.92 4.33 C74.45 4.86, 75.85 5.45, 77.04 6.05 C78.24 6.66, 79.27 7.31, 80.09 7.97 C80.9 8.63, 81.53 9.32, 81.95 10.01 C82.36 10.7, 82.47 11.76, 82.58 12.11 C82.68 12.46, 82.68 11.76, 82.58 12.11" stroke="none" stroke-width="0" fill="#fff9db"></path><path d="M82.58 12.11 C82.58 12.81, 82.36 13.52, 81.95 14.21 C81.53 14.9, 80.9 15.59, 80.09 16.25 C79.27 16.91, 78.24 17.56, 77.04 18.16 C75.85 18.77, 74.45 19.36, 72.92 19.89 C71.38 20.43, 69.66 20.93, 67.83 21.39 C66 21.84, 64 22.25, 61.93 22.6 C59.86 22.95, 57.66 23.25, 55.41 23.49 C53.16 23.73, 50.81 23.91, 48.46 24.03 C46.1 24.16, 43.68 24.22, 41.29 24.22 C38.9 24.22, 36.47 24.16, 34.12 24.03 C31.77 23.91, 29.41 23.73, 27.17 23.49 C24.92 23.25, 22.71 22.95, 20.64 22.6 C18.57 22.25, 16.58 21.84, 14.75 21.39 C12.92 20.93, 11.2 20.43, 9.66 19.89 C8.12 19.36, 6.73 18.77, 5.53 18.16 C4.34 17.56, 3.31 16.91, 2.49 16.25 C1.67 15.59, 1.04 14.9, 0.63 14.21 C0.21 13.52, 0 12.81, 0 12.11 C0 11.41, 0.21 10.7, 0.63 10.01 C1.04 9.32, 1.67 8.63, 2.49 7.97 C3.31 7.31, 4.34 6.66, 5.53 6.05 C6.73 5.45, 8.12 4.86, 9.66 4.33 C11.2 3.79, 12.92 3.28, 14.75 2.83 C16.58 2.38, 18.57 1.97, 20.64 1.62 C22.71 1.27, 24.92 0.97, 27.17 0.73 C29.41 0.49, 31.77 0.31, 34.12 0.18 C36.47 0.06, 38.9 0, 41.29 0 C43.68 0, 46.1 0.06, 48.46 0.18 C50.81 0.31, 53.16 0.49, 55.41 0.73 C57.66 0.97, 59.86 1.27, 61.93 1.62 C64 1.97, 66 2.38, 67.83 2.83 C69.66 3.28, 71.38 3.79, 72.92 4.33 C74.45 4.86, 75.85 5.45, 77.04 6.05 C78.24 6.66, 79.27 7.31, 80.09 7.97 C80.9 8.63, 81.53 9.32, 81.95 10.01 C82.36 10.7, 82.47 11.76, 82.58 12.11 C82.68 12.46, 82.68 11.76, 82.58 12.11" stroke="#ffd43b" stroke-width="2" fill="none"></path></g><g stroke-linecap="round"><g transform="translate(161.87293086790663 60.5849028842938) rotate(0 27.33925080121719 0)"><path d="M0 0 C20.57 0, 41.13 0, 54.68 0 M0 0 C12.3 0, 24.6 0, 54.68 0" stroke="#1e1e1e" stroke-width="2" fill="none"></path></g><g transform="translate(161.87293086790663 60.5849028842938) rotate(0 27.33925080121719 0)"><path d="M31.19 8.55 C40.02 5.33, 48.86 2.12, 54.68 0 M31.19 8.55 C36.47 6.63, 41.76 4.7, 54.68 0" stroke="#1e1e1e" stroke-width="2" fill="none"></path></g><g transform="translate(161.87293086790663 60.5849028842938) rotate(0 27.33925080121719 0)"><path d="M31.19 -8.55 C40.02 -5.33, 48.86 -2.12, 54.68 0 M31.19 -8.55 C36.47 -6.63, 41.76 -4.7, 54.68 0" stroke="#1e1e1e" stroke-width="2" fill="none"></path></g></g><mask></mask><g stroke-linecap="round"><g transform="translate(369.92652415438266 61.17002749377821) rotate(0 26.90458680560062 0)"><path d="M0 0 C20.2 0, 40.4 0, 53.81 0 M0 0 C13.32 0, 26.64 0, 53.81 0" stroke="#1e1e1e" stroke-width="2" fill="none"></path></g><g transform="translate(369.92652415438266 61.17002749377821) rotate(0 26.90458680560062 0)"><path d="M30.32 8.55 C39.13 5.34, 47.95 2.13, 53.81 0 M30.32 8.55 C36.13 6.43, 41.95 4.32, 53.81 0" stroke="#1e1e1e" stroke-width="2" fill="none"></path></g><g transform="translate(369.92652415438266 61.17002749377821) rotate(0 26.90458680560062 0)"><path d="M30.32 -8.55 C39.13 -5.34, 47.95 -2.13, 53.81 0 M30.32 -8.55 C36.13 -6.43, 41.95 -4.32, 53.81 0" stroke="#1e1e1e" stroke-width="2" fill="none"></path></g></g><mask></mask><g stroke-linecap="round"><g transform="translate(289.98599321782154 102.08354688807412) rotate(0 0 29.83052102649333)"><path d="M0 0 C0 16.48, 0 32.97, 0 59.66 M0 0 C0 14.32, 0 28.64, 0 59.66" stroke="#1e1e1e" stroke-width="2" fill="none"></path></g><g transform="translate(289.98599321782154 102.08354688807412) rotate(0 0 29.83052102649333)"><path d="M-8.55 36.17 C-6.19 42.66, -3.83 49.15, 0 59.66 M-8.55 36.17 C-6.5 41.81, -4.45 47.44, 0 59.66" stroke="#1e1e1e" stroke-width="2" fill="none"></path></g><g transform="translate(289.98599321782154 102.08354688807412) rotate(0 0 29.83052102649333)"><path d="M8.55 36.17 C6.19 42.66, 3.83 49.15, 0 59.66 M8.55 36.17 C6.5 41.81, 4.45 47.44, 0 59.66" stroke="#1e1e1e" stroke-width="2" fill="none"></path></g></g><mask></mask><g stroke-linecap="round"><g transform="translate(90.09207282255929 102.39623569341279) rotate(0 62.32970244835191 50.8946957944388)"><path d="M0 0 C47.28 38.6, 94.55 77.21, 124.66 101.79 M0 0 C30.21 24.67, 60.43 49.34, 124.66 101.79" stroke="#1e1e1e" stroke-width="2" fill="none"></path></g><g transform="translate(90.09207282255929 102.39623569341279) rotate(0 62.32970244835191 50.8946957944388)"><path d="M101.05 93.55 C110.01 96.68, 118.96 99.8, 124.66 101.79 M101.05 93.55 C106.78 95.55, 112.5 97.55, 124.66 101.79" stroke="#1e1e1e" stroke-width="2" fill="none"></path></g><g transform="translate(90.09207282255929 102.39623569341279) rotate(0 62.32970244835191 50.8946957944388)"><path d="M111.87 80.31 C116.72 88.45, 121.57 96.6, 124.66 101.79 M111.87 80.31 C114.97 85.51, 118.07 90.72, 124.66 101.79" stroke="#1e1e1e" stroke-width="2" fill="none"></path></g></g><mask></mask><g stroke-linecap="round"><g transform="translate(499.1192703262658 101.54127155260176) rotate(0 -65.73959661702042 52.050147839022316)"><path d="M0 0 C-37.31 29.54, -74.62 59.08, -131.48 104.1 M0 0 C-36.19 28.65, -72.37 57.3, -131.48 104.1" stroke="#1e1e1e" stroke-width="2" fill="none"></path></g><g transform="translate(499.1192703262658 101.54127155260176) rotate(0 -65.73959661702042 52.050147839022316)"><path d="M-118.37 82.81 C-122.09 88.85, -125.81 94.89, -131.48 104.1 M-118.37 82.81 C-121.98 88.67, -125.59 94.53, -131.48 104.1" stroke="#1e1e1e" stroke-width="2" fill="none"></path></g><g transform="translate(499.1192703262658 101.54127155260176) rotate(0 -65.73959661702042 52.050147839022316)"><path d="M-107.75 96.22 C-114.49 98.46, -121.22 100.69, -131.48 104.1 M-107.75 96.22 C-114.28 98.39, -120.81 100.56, -131.48 104.1" stroke="#1e1e1e" stroke-width="2" fill="none"></path></g></g><mask></mask><g stroke-linecap="round"><g transform="translate(577.3124555066081 61.160802293765755) rotate(0 28.11195368791266 0)"><path d="M0 0 C21.96 0, 43.92 0, 56.22 0 M0 0 C20.11 0, 40.22 0, 56.22 0" stroke="#1e1e1e" stroke-width="2" fill="none"></path></g><g transform="translate(577.3124555066081 61.160802293765755) rotate(0 28.11195368791266 0)"><path d="M32.73 8.55 C41.91 5.21, 51.08 1.87, 56.22 0 M32.73 8.55 C41.13 5.49, 49.53 2.43, 56.22 0" stroke="#1e1e1e" stroke-width="2" fill="none"></path></g><g transform="translate(577.3124555066081 61.160802293765755) rotate(0 28.11195368791266 0)"><path d="M32.73 -8.55 C41.91 -5.21, 51.08 -1.87, 56.22 0 M32.73 -8.55 C41.13 -5.49, 49.53 -2.43, 56.22 0" stroke="#1e1e1e" stroke-width="2" fill="none"></path></g></g><mask></mask><g transform="translate(208.58786010742162 275.1878809224304) rotate(0 252.36526489257812 9.200000000000045)"><text x="252.36526489257812" y="0" font-family="Helvetica, Segoe UI Emoji" font-size="16px" fill="#1e1e1e" text-anchor="middle" style="white-space: pre;" direction="ltr" dominant-baseline="text-before-edge">출처: 스프링 입문 - 코드로 배우는 스프링 부트, 웹 MVC, DB 접근 기술 (김영한)</text></g></svg>

- 컨트롤러: 웹 MVC의 컨트롤러 역할
- 서비스: 도메인을 이용하여 핵심 비즈니스 로직 구현
- 리포지토리: 데이터베이스에 접근, 도메인 객체를 DB에 저장하고 관리
- 도메인: 비즈니스 도메인 객체, DB에 저장하고 관리
  - 예) 회원, 쿠폰, 주문 등등

# 클래스 의존관계
<svg version="1.1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 529.1898166089417 281.26593898499027" width="529.1898166089417" height="281.26593898499027">
  <!-- svg-source:excalidraw -->
  
  <defs>
    <style class="style-fonts">
      @font-face {
        font-family: "Virgil";
        src: url("https://excalidraw.com/Virgil.woff2");
      }
      @font-face {
        font-family: "Cascadia";
        src: url("https://excalidraw.com/Cascadia.woff2");
      }
      @font-face {
        font-family: "Assistant";
        src: url("https://excalidraw.com/Assistant-Regular.woff2");
      }
    </style>
    
  </defs>
  <rect x="0" y="0" width="529.1898166089417" height="281.26593898499027" fill="#ffffff"></rect><g stroke-linecap="round" transform="translate(10 10) rotate(0 75.98331674657287 39.668400582715435)"><path d="M0 0 C47.82 0, 95.65 0, 151.97 0 M0 0 C54.62 0, 109.25 0, 151.97 0 M151.97 0 C151.97 30.3, 151.97 60.61, 151.97 79.34 M151.97 0 C151.97 16.18, 151.97 32.36, 151.97 79.34 M151.97 79.34 C109.94 79.34, 67.92 79.34, 0 79.34 M151.97 79.34 C121.57 79.34, 91.16 79.34, 0 79.34 M0 79.34 C0 52.14, 0 24.95, 0 0 M0 79.34 C0 62.96, 0 46.59, 0 0" stroke="#1e1e1e" stroke-width="2" fill="none"></path></g><g transform="translate(29.967691746572882 40.4684005827155) rotate(0 56.015625 9.200000000000045)"><text x="56.015625" y="0" font-family="Helvetica, Segoe UI Emoji" font-size="16px" fill="#1e1e1e" text-anchor="middle" style="white-space: pre;" direction="ltr" dominant-baseline="text-before-edge">MemgerService</text></g><g stroke-linecap="round" transform="translate(364.81372063739644 10.923408687580377) rotate(0 75.98331674657288 39.668400582715435)"><path d="M0 0 C40.23 0, 80.46 0, 151.97 0 M0 0 C48.55 0, 97.1 0, 151.97 0 M151.97 0 C151.97 22.43, 151.97 44.86, 151.97 79.34 M151.97 0 C151.97 28.57, 151.97 57.14, 151.97 79.34 M151.97 79.34 C93.73 79.34, 35.49 79.34, 0 79.34 M151.97 79.34 C117.29 79.34, 82.62 79.34, 0 79.34 M0 79.34 C0 53.29, 0 27.23, 0 0 M0 79.34 C0 53.15, 0 26.97, 0 0" stroke="#1e1e1e" stroke-width="2" fill="none"></path></g><g transform="translate(373.2189123839693 32.191809270295835) rotate(0 67.578125 18.399999999999977)"><text x="67.578125" y="0" font-family="Helvetica, Segoe UI Emoji" font-size="16px" fill="#1e1e1e" text-anchor="middle" style="white-space: pre;" direction="ltr" dominant-baseline="text-before-edge">interface</text><text x="67.578125" y="18.4" font-family="Helvetica, Segoe UI Emoji" font-size="16px" fill="#1e1e1e" text-anchor="middle" style="white-space: pre;" direction="ltr" dominant-baseline="text-before-edge">MemberRepository</text></g><g stroke-linecap="round" transform="translate(366.350022790797 151.21299834685715) rotate(0 75.98331674657288 39.668400582715435)"><path d="M0 0 C52.49 0, 104.97 0, 151.97 0 M0 0 C30.99 0, 61.98 0, 151.97 0 M151.97 0 C151.97 21.61, 151.97 43.23, 151.97 79.34 M151.97 0 C151.97 31.59, 151.97 63.19, 151.97 79.34 M151.97 79.34 C106.16 79.34, 60.36 79.34, 0 79.34 M151.97 79.34 C118.73 79.34, 85.5 79.34, 0 79.34 M0 79.34 C0 62.09, 0 44.84, 0 0 M0 79.34 C0 49.19, 0 19.04, 0 0" stroke="#1e1e1e" stroke-width="2" fill="none"></path></g><g transform="translate(374.7552145373699 172.4813989295726) rotate(0 67.578125 18.399999999999977)"><text x="67.578125" y="0" font-family="Helvetica, Segoe UI Emoji" font-size="16px" fill="#1e1e1e" text-anchor="middle" style="white-space: pre;" direction="ltr" dominant-baseline="text-before-edge">Memory</text><text x="67.578125" y="18.4" font-family="Helvetica, Segoe UI Emoji" font-size="16px" fill="#1e1e1e" text-anchor="middle" style="white-space: pre;" direction="ltr" dominant-baseline="text-before-edge">MemberRepository</text></g><g stroke-linecap="round"><g transform="translate(162.96663349314574 49.709482515898344) rotate(0 100.94594220671985 0)"><path d="M0 0 C68.35 0, 136.7 0, 201.89 0 M0 0 C67.54 0, 135.07 0, 201.89 0" stroke="#1e1e1e" stroke-width="2" fill="none"></path></g><g transform="translate(162.96663349314574 49.709482515898344) rotate(0 100.94594220671985 0)"><path d="M178.4 8.55 C186.35 5.66, 194.31 2.76, 201.89 0 M178.4 8.55 C186.26 5.69, 194.12 2.83, 201.89 0" stroke="#1e1e1e" stroke-width="2" fill="none"></path></g><g transform="translate(162.96663349314574 49.709482515898344) rotate(0 100.94594220671985 0)"><path d="M178.4 -8.55 C186.35 -5.66, 194.31 -2.76, 201.89 0 M178.4 -8.55 C186.26 -5.69, 194.12 -2.83, 201.89 0" stroke="#1e1e1e" stroke-width="2" fill="none"></path></g></g><mask></mask><g transform="translate(14.459286823785419 252.86593898499018) rotate(0 252.36526489257812 9.200000000000045)"><text x="252.36526489257812" y="0" font-family="Helvetica, Segoe UI Emoji" font-size="16px" fill="#1e1e1e" text-anchor="middle" style="white-space: pre;" direction="ltr" dominant-baseline="text-before-edge">출처: 스프링 입문 - 코드로 배우는 스프링 부트, 웹 MVC, DB 접근 기술 (김영한)</text></g><g stroke-linecap="round"><g transform="translate(442.694594518008 151.5461266137811) rotate(0 0 -30.06161950769001)"><path d="M0 0 C-1.47 -20.99, 2 -44.64, 0 -60.12" stroke="#1e1e1e" stroke-width="2.5" fill="none" stroke-dasharray="1.5 8"></path></g><g transform="translate(442.694594518008 151.5461266137811) rotate(0 0 -30.06161950769001)"><path d="M-1.33 -60.25 L5.31 -45.95 L-5.79 -46.94 L1.11 -59" stroke="none" stroke-width="0" fill="#1e1e1e" fill-rule="evenodd"></path><path d="M0 -60.12 C0.89 -54.52, 6 -50.96, 6.85 -46.78 M6.85 -46.78 C4.66 -45.72, 1.28 -46.9, -5.82 -46.3 M-5.82 -46.3 C-3.82 -50.94, -3.76 -52.31, 0 -60.12 M0 -60.12 C0 -60.12, 0 -60.12, 0 -60.12" stroke="#1e1e1e" stroke-width="2.5" fill="none"></path></g></g><mask></mask></svg>

- 인터페이스로 구현 클래스를 변경할 수 있도록 설계
- 가벼운 개발을 위해 초기 개발 단계에서는 가벼운 메모리 기반의 데이터 저장소 사용

# 회원 도메인과 리포지토리 만들기

> 깃허브 리포지토리 주소: <https://github.com/nyj001012/springboot_tutorial>

## 도메인 만들기
```java
package hello.hellospring.domain;

import java.util.concurrent.atomic.AtomicLong;

public class Member {
    private Long id;
    private String name;

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }
}

```

## 리포지토리 만들기
### 리포지토리 인터페이스
```java
package hello.hellospring.repository;

import hello.hellospring.domain.Member;

import java.util.List;
import java.util.Optional;
import java.util.concurrent.atomic.AtomicLong;

public interface MemberRepository {
    Member save(Member member);
    Optional<Member> findById(Long id);
    Optional<Member> findByName(String name);
    List<Member> findAll();
}

```

### 메모리 리포지토리
```java
package hello.hellospring.repository;

import hello.hellospring.domain.Member;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicLong;

public class MemoryMemberRepository implements MemberRepository {
    private static ConcurrentHashMap<Long, Member> store = new ConcurrentHashMap<>();
    private static AtomicLong sequence = new AtomicLong(0);

    @Override
    public Member save(Member member) {
        sequence.incrementAndGet();
        member.setId(sequence.longValue());
        store.put(sequence.longValue(), member);
        return member;
    }

    @Override
    public Optional<Member> findById(long id) {
        return Optional.ofNullable(store.get(id));
    }

    @Override
    public Optional<Member> findByName(String name) {
        return store.values()
                .stream()
                .filter(member -> member.getName().equals(name))
                .findAny();
    }

    @Override
    public List<Member> findAll() {
        return new ArrayList<Member>(store.values());
    }

    public void clearStore() {
        store.clear();
        sequence = new AtomicLong(0);
    }
}

```

원래 강의에서는 `AtomicLong` 대신 `Long`을 사용하였는데, 강의에서 "실무에서는 동시성 문제 때문에 `AtomicLong`을 사용하지만, 여기서는 간단하게 `Long`을 사용하겠다."는 말을 듣고 궁금해서 사용했다. 이 부분에 대해서는 따로 포스트를 작성하도록 하겠다.

`AtomicLong`과 마찬가지로 `ConcurrentHashMap` 또한 같은 이유에서 사용했다.

### 테스트 코드 작성
```java
package hello.hellospring.repository;

import hello.hellospring.domain.Member;
import org.junit.jupiter.api.*;

import java.util.List;
import java.util.Optional;

import static org.assertj.core.api.Assertions.*;

public class MemoryMemberRepositoryTest {
    MemoryMemberRepository repository = new MemoryMemberRepository();

    @AfterEach
    void afterEach() {
        repository.clearStore();
    }

    @Nested
    class TestSave {
        @Test
        void save() {
            Member yejin = new Member();
            yejin.setName("예진");
            Member saveResult = repository.save(yejin);
            assertThat(saveResult).isEqualTo(yejin);
            assertThat(saveResult.getId().longValue()).isEqualTo(1);
        }
    }

    @Nested
    class TestExcludeSave {
        @BeforeEach
        void beforeEach() {
            Member yejin = new Member();
            Member yena = new Member();
            yejin.setName("예진");
            yena.setName("예나");
            repository.save(yejin);
            repository.save(yena);
        }

        @Test
        void findById() {
            Optional<Member> findResult = repository.findById(1L);
            Member member = findResult.orElse(null);
            assertThat(member).isNotNull();
            assertThat(member.getName()).isEqualTo("예진");
        }

        @Test
        void findByIdFail() {
            Optional<Member> findResult = repository.findById(-2L);
            assertThat(findResult.isEmpty()).isTrue();
        }

        @Test
        void findByName() {
            Optional<Member> findResult = repository.findByName("예진");
            Member member = findResult.orElse(null);
            assertThat(member).isNotNull();
            assertThat(member.getId()).isEqualTo(1);
        }

        @Test
        void findByNameFail() {
            Optional<Member> findResult = repository.findByName("고구마");
            assertThat(findResult.isEmpty()).isTrue();
        }

        @Test
        void findAll() {
            List<Member> memberList = repository.findAll();
            assertThat(memberList.size()).isEqualTo(2);
        }
    }
}

```

테스트 코드도 강의보다는 조금 더 자세하게 작성했다.
`@BeforeEach`로 각 테스트 케이스가 시작되기 전에, `repository`에 데이터를 저장하는 일을 했다.

`save()`함수 테스트 케이스 동작 시 기존 `repository`에 데이터를 저장하는 작업이 필요 없어서, `@Nested` 어노테이션을 이용하여 미리 `repository`에 데이터를 저장해야하는 케이스들과 아닌 케이스들로 나누었다.

`@AfterEach`로는 `repository`를 초기화하는 역할을 하기 때문에, 모든 `@Nested` 클래스에게 똑같이 적용되도록 중첩 클래스 바깥에 정의해두었다.

# 회원 서비스 작성
```java
package hello.hellospring.service;

import hello.hellospring.domain.Member;
import hello.hellospring.repository.MemberRepository;
import hello.hellospring.repository.MemoryMemberRepository;

import java.util.List;
import java.util.Optional;

public class MemberService {
    public MemberService(MemberRepository memberRepository) {
        this.memberRepository = memberRepository;
    }

    private final MemberRepository memberRepository;

    /**
     * 회원 가입
     *
     * @param member 가입할 멤버 객체
     * @return 가입한 멤버 객체의 id
     */
    public Long join(Member member) {
        validateDuplicateMember(member);

        memberRepository.save(member);
        return member.getId();
    }

    /**
     * 중복 회원 검사
     * @param member 검사할 회원
     */
    private void validateDuplicateMember(Member member) {
        memberRepository.findByName(member.getName())
                .ifPresent(m -> {
                    throw new IllegalStateException("이미 존재하는 회원입니다.");
                });
    }

    /**
     * 전체 회원 조회
     * @return 전체 회원 리스트
     */
    public List<Member> findMembers() {
        return memberRepository.findAll();
    }

    /**
     * id로 한 회원 조회
     * @param memberId 조회할 회원의 Id
     * @return Member의 Optional 객체
     */
    public Optional<Member> findOneById(Long memberId) {
        return memberRepository.findById(memberId);
    }
}

```

## 테스트 작성
```java
package hello.hellospring.service;

import hello.hellospring.domain.Member;
import hello.hellospring.repository.MemoryMemberRepository;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.Optional;

import static org.assertj.core.api.Assertions.assertThat;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.fail;


class MemberServiceTest {
    MemberService memberService;
    MemoryMemberRepository memoryMemberRepository;

    @BeforeEach
    void setUp() {
        memoryMemberRepository = new MemoryMemberRepository();
        memberService = new MemberService(memoryMemberRepository);
    }

    @AfterEach
    void tearDown() {
        memoryMemberRepository.clearStore();
    }

    @Test
    void 회원가입() {
        Member member = new Member();
        member.setName("에진");

        memberService.join(member);

        Optional<Member> findResult = memoryMemberRepository.findByName(member.getName());
        Member joinedMember = findResult.get();
        assertThat(member.getName()).isEqualTo(joinedMember.getName());
    }

    @Test
    void 회원가입_중복_유저() {
        Member member1 = new Member();
        Member member2 = new Member();
        member1.setName("예진");
        member2.setName("예진");

        memberService.join(member1);

        IllegalStateException e = assertThrows(IllegalStateException.class, () -> memberService.join(member2));
        assertThat(e.getMessage()).isEqualTo("이미 존재하는 회원입니다.");
    }

    @Test
    void 모든_멤버_리스트_가져오기() {
        for (int i = 0; i < 10; i++) {
            Member member = new Member();
            member.setName(Integer.toString(i) + "번째 유저");
            memberService.join(member);
        }

        List<Member> members = memberService.findMembers();

        assertThat(members.size()).isEqualTo(10);
    }

    @Test
    void id로_멤버_찾기() {
        Member member1 = new Member();
        Member member2 = new Member();
        member1.setName("피카츄");
        member2.setName("리자몽");
        memberService.join(member1);
        memberService.join(member2);

        Optional<Member> findResult = memberService.findOneById(member1.getId());

        findResult.ifPresentOrElse(member -> {
            assertThat(member.getName()).isEqualTo(member1.getName());
        }, () -> {
            fail();
        });
    }

    @Test
    void 없는_id로_멤버_찾기() {
        Member member1 = new Member();
        member1.setName("피카츄");
        memberService.join(member1);

        Optional<Member> findResult = memberService.findOneById(-1L);

        assertThat(findResult.isEmpty()).isTrue();
    }
}

```

테스트 함수 한글로 적어도 된다니 신세계다..! 이번 서비스 함수의 테스트 코드를 작성해보면서 예외 처리 테스트는 어떻게 작성할 수 있는지를 알 수 있었다.

또한 Service 객체에서 Repository 객체를 가지고 있는데, 이를 테스트 단계에서 따로 만들어서 사용하면 별개의 Repository 객체가 생겨버린다. 때문에 의존성 주입을 통해 Service 객체의 생성자의 매개변수로 Repository 객체를 넘겨줌으로써 해결할 수 있었다.

테스트 꿀잼
