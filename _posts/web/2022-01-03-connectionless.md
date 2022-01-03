---
title: "비 연결성"
excerpt: "HTTP 웹 기본 지식"
category: 
  - web
author_profile: true
sidebar:
  - nav: "main" 
tag:
  - http
  - connectionless
toc: true
toc_sticky: true
---
> 이 포스트는 김영한님의 ['모든 개발자를 위한 HTTP 웹 기본 지식'](https://www.inflearn.com/course/http-%EC%9B%B9-%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%81%AC)을 수강하고 작성하였습니다.  

# 연결 유지 vs 비 연결
## 연결 유지
![connection](/assets/images/page/web/2022-01-03_connect.png)

서버는 응답이 끝난 뒤에도 클라이언트와의 연결을 계속 유지한다.

## 비 연결
![connectionless](/assets/images/page/web/2022-01-03_connectionless.png)

서버는 응답이 끝나면 클라이언트와의 연결을 끊음으로써 최소한의 자원을 유지한다.

# 비 연결성 (Connectionless)
> stateless가 떠오르는 특성이다. 연결을 유지하지 않으니 한 번에 추가적인 데이터까지 모두 전달해야 하지 않을까 해서.

## 특징
- HTTP는 기본적으로 연결을 유지하지 않는 모델이다.
- 일반적으로 초 단위 이하의 빠른 속도로 응답한다.
- 1시간 동안 수천 명이 서비스를 사용해도, 실제 서버에서 동시에 처리하는 요청은 수십 개 이하로 매우 적다.
- 서버 자원을 매우 효율적으로 사용할 수 있다.

## 한계와 극복
- TCP/IP 연결을 새로 맺어야 한다. 이는 3 way handshake의 시간이 늘어남을 의미한다.
- 웹 브라우저로 사이트를 요청하면 HTML 뿐만 아니라 자바 스크립트, css, 추가 이미지 등, 수많은 자원이 함께 다운로드된다.
- 지금은 HTTP 지속 연결(Persistent Connections)로 문제를 해결했다.
- HTTP/2, HTTP/3에서 더 많은 최적화가 이루어져 속도가 개선되었다.

# HTTP 지속 연결 (Persistent Connections)
![persistent_conn](/assets/images/page/web/2022-01-03_persistent.png)

연결을 하고 웬만한 HTML 페이지를 다 받을 때까지 연결을 유지한다.

# 스테이스리스는 기억할 것입니다.
> 서버 개발자들이 어려워하는 업무라고 한다. 실제로 채용공고를 살펴보면 대용량 트래픽 처리 경험이 있는지를 묻는다.

- 같은 시간에 딱 맞춰 발생하는 대용량 트래픽
  - 예) 선착순 이벤트(오늘 체크인 미팅 신청하고 왔다. 사람 너무 많아), 명절 KTX 예약, 수강신청  

과 같은 상황에서는 스테이스리스를 사용하면 서버를 증설하기도 쉽다. 귀찮고 머리 아프더라도 스테이스리스를 고려하여 개발하자.