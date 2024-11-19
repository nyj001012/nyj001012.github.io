---
title: "리액트를 처음 사용하며"
excerpt: "리액트를 처음 사용하며 겪은 일들"
category: 
  - web
  - react
author_profile: true
sidebar:
  - nav: "main" 
tag:
  - web
  - react
  - 이터널 리턴
  - 밸런스 게임
toc: true
toc_sticky: true
last_modified_at: 2024-11-19T00:00:00+09:00
---

# 왜 리액트?
이터널 리턴 밸런스 게임 프로젝트를 하면서 백엔드는 기본적인 질문 생성, 선택 API는 다 작성했다.  
그래서 이제 화면을 그리기 위해 프론트엔드를 어떻게 만들지 고민하고 있었다.  

가장 빨리 만드는 것(html, js)과 그래도 실무에서 사용하는 것(리액트) 중 뭘 고를까 생각해봤는데, 일일이 페이지를 html로 작성하는 건 귀찮고 집현전에서 아아주 잠깐 리액트를 찍어 먹어 본 경험이 있었기에 리액트로 결정했다.

# 설치
## Nextjs, Remix, Gatsby, Expo
> 공식문서: <https://react.dev/learn/typescript#installation>

리액트를 설치하기 위해 공식 문서를 찾아봤는데, 리액트 라이브러리를 사용하는 데 도움을 주는 프레임워크인 Nextjs, Remix, Gatsby, Expo를 추천하고 있었다.

그중 Nextjs, Expo를 골라서 설치를 해봤는데, 폴더 구조를 보니 Nextjs는 프론트엔드 및 백엔드를 지원하는 것 같았다.  
그리고 난 가벼운 프론트엔드 프로젝트, 딱 백엔드에 요청 보내고 받아서 화면에 뿌려주기만을 바랐기 때문에 그에 비해 Nextjs쪽은 너무 무거운 것 같았다.

Expo로 설치한 건 사실 파일명이 `index`였나, 거기에 작성된 코드를 살펴봤는데 조금 기간을 두고 공부해야할 것 같아서 나름 짧은 기간 내에 만들어야하는 나에겐 적절하지 않은 것 같았다.

그래서 구글링을 좀 해보니 CRA로 리액트 프로젝트를 초기화하는 것을 보고 그걸 사용하기로 했다.

## CRA
> 공식문서: <https://reactjs-kr.firebaseapp.com/docs/installation.html#creating-a-new-application>

```bash
npx create-react-app my-app
```

`create-react-app`(CRA)을 사용하는 방법인데, 사실 GPT에게 물어보니 최신 리액트에서는 권장하지 않는 방법이라고 한다. 그러면서 대안으로 Vite와 Nextjs로 설치하는 방법을 알려주는데, Nextjs는 무거워서 패스하고 Vite로 설치하기로 했다.

## Vite
> 공식 문서: <https://ko.vite.dev/guide/why.html>

Vite(비트라고 읽는다. 헉)는 사전 번들링으로 Esbuild를 사용해서 기존 번들러보다 훨씬 빠르다. 또한 브라우저가 요청하는 대로 소스 코드를 변환하고 제공하기 때문에 서버 구동에 걸리는 시간을 줄였다.  

Vite는 수정된 모듈과 관련된 부분만 교체하고, HTTP 헤더를 활용하여 전체 페이지의 로드 속도를 높이고, 캐싱으로 요청 횟수를 최소화하기 때문에 소스 코드 갱신이 빠르다.

### Vite 사용
```bash
npm create vite@latest my-app
```

이 명령을 실행하면 프레임워크를 선택하라는 메시지가 나오는데, 여기에서 리액트를 선택한다(응?).

```bash
> create-vite my-app

? Select a framework: › - Use arrow-keys. Return to submit.
❯   Vanilla
    Vue
    React
    Preact
    Lit
    Svelte
    Solid
    Qwik
    Angular
    Others
```

그리고 Variant를 선택하라 나오는데, 난 여기서 Typescript를 선택했다.

```bash
? Select a variant: › - Use arrow-keys. Return to submit.
❯   TypeScript
    TypeScript + SWC
    JavaScript
    JavaScript + SWC
    Remix ↗
```

다 선택했으면 설치가 끝나고 아래와 같이 명령어를 사용해서 실행하라고 알려준다.

```bash
> my-app@0.0.0 npx
> create-vite my-app

✔ Select a framework: › React
✔ Select a variant: › TypeScript

Scaffolding project in /Users/nayejin/dev/react_tutorial/tutorial/my-app/my-app...

Done. Now run:

  cd my-app
  npm install
  npm run dev
```

### SWC
> 공식 문서: <https://swc.rs/>

SWC는 Rust 기반 컴파일러로, Babel보다 20배 빠르다고 한다.
그런데 다른 라이브러리들과의 호환성이 떨어지는 경우가 있다길래 SWC는 사용하지 않기로 했다.
