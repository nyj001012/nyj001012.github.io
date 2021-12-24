---
title: "웹 브라우저 요청 흐름"
excerpt: "HTTP 웹 기본 지식"
category: 
  - web
author_profile: true
sidebar:
  - nav: "main" 
tag:
  - http
  - web browser
toc: true
toc_sticky: true
---
> 이 포스트는 김영한님의 ['모든 개발자를 위한 HTTP 웹 기본 지식'](https://www.inflearn.com/course/http-%EC%9B%B9-%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%81%AC)을 수강하고 작성하였습니다.  

# 웹 브라우저 요청 흐름
## HTTP 요청 메시지 생성
![request](/assets/images/page/web/2021-12-24_browser_flow1.png)

1. 웹 브라우저에서 구글 서버로 보낼 HTTP 요청 메시지를 생성한다.
  
ex) HTTP 요청 메시지  

```
GET /search?q=hello&hl=ko HTTP/1.1  
Host: www.google.com
```

## HTTP 요청 메시지 전송
![transmit](/assets/images/page/web/2021-12-24_browser_flow2.png)

2. 웹 브라우저에서 생성된 HTTP 메시지를 SOCKET 라이브러리를 통해 OS 계층으로 전달한다.
3. TCP/IP 패킷을 생성하고, 패킷에 HTTP 메시지를 담는다.
4. LAN 드라이버, LAN 장비 등의 네트워크 인터페이스로 인터넷을 통해 서버로 전송한다.

## HTTP 응답 메시지 생성
5. 웹 브라우저가 전달한 요청 패킷이 서버에 도착한다.
6. 서버는 웹 브라우저에 전달할 HTTP 응답 메시지를 생성한다.  

ex) HTTP 응답 메시지

```html
HTTP/1.1 200OK  
Content-Type: text/html;charset=UTF-8  
Content-Length: 3423  
<html>  
  <body></body>  
</html>  
```

## HTTP 응답 메시지 전송
![response](/assets/images/page/web/2021-12-24_browser_flow3.png)

7. 서버가 웹 브라우저에게 응답 메시지를 전송한다.

## 웹 브라우저 렌더링
![rendering](/assets/images/page/web/2021-12-24_browser_flow4.png)

8. 웹 브라우저는 서버로부터 받은 HTTP 응답 메시지(HTML)를 렌더링한다.