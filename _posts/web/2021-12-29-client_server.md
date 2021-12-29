---
title: "클라이언트-서버 구조"
excerpt: "HTTP 웹 기본 지식"
category: 
  - web
author_profile: true
sidebar:
  - nav: "main" 
tag:
  - http
  - client
  - server
  - client server architecture
toc: true
toc_sticky: true
---
> 이 포스트는 김영한님의 ['모든 개발자를 위한 HTTP 웹 기본 지식'](https://www.inflearn.com/course/http-%EC%9B%B9-%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%81%AC)을 수강하고 작성하였습니다.  

# 클라이언트-서버 구조
> 학교 다닐 때 배웠던 3-Tier archtecture랑 비슷하려나

![client_server](/assets/images/page/web/2021-12-29_client-server.png)
- Request Response 구조
- 클라이언트는 서버에 요청(Request)을 보내고, 응답(Response)을 대기
- 서버가 요청에 대한 결과를 만들어서 응답

## 클라이언트와 서버를 분리한 이유
- 클라이언트와 서버가 독립적으로 동작할 수 있다.
  - 대규모 트래픽을 처리할 때, 클라이언트는 냅두고 서버에서 작업한다.