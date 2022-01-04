---
title: "HTTP 메시지"
excerpt: "HTTP 웹 기본 지식"
category: 
  - web
author_profile: true
sidebar:
  - nav: "main" 
tag:
  - http
  - http message
toc: true
toc_sticky: true
---
> 이 포스트는 김영한님의 ['모든 개발자를 위한 HTTP 웹 기본 지식'](https://www.inflearn.com/course/http-%EC%9B%B9-%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%81%AC)을 수강하고 작성하였습니다.  

# HTTP 메시지 구조
![http_message_structure](/assets/images/page/web/2022-01-04_http_msg1.png)
![http_response_structure](/assets/images/page/web/2022-01-04_http_res_msg1.png)

## start-line
### request-line - HTTP 요청 메시지
> GET /search?q=hello&hl=ko HTTP/1.1  
> method SP(공백) request-target SP HTTP-version CRLF(엔터)

- method - HTTP 메서드
  - GET, POST, PUT, DELETE, etc...
  - 서버가 수행해야 할 동작을 지정한다.
    - GET: 리소스 조회
    - POST: 요청 내역 처리
- request-target - 요청 대상
  - absolute-path[?query] (절대경로[?쿼리])
  - 절대경로: '/'로 시작하는 경로
  - 참고: *, http://..?x=y와 같이 다른 유형의 경로지정 방법도 있다.
- HTTP-version

### status-line - HTTP 응답 메시지
> HTTP/1.1 200 OK  
> HTTP-version SP status-code SP reason-phrase CRLF

- HTTP-version
- HTTP status code: 요청 성공, 실패를 나타낸다.
  - 200: 성공
  - 400: 클라이언트 요청 오류
  - 500: 서버 내부 오류
- reason-phrase
  - 사람이 이해할 수 있는 짧은 상태 코드 설명 글(자연어)

## HTTP 헤더
![http_msg_header](/assets/images/page/web/2022-01-04_http_msg_header.png)
- HTTP 전송에 필요한 모든 부가정보를 포함한다.
  - 예) 메시지 바디의 내용, 메시지 바디의 크기, 압축, 인증 정보, 요청 클라이언트(브라우저) 정보, 서버 어플리케이션 정보, 캐시 관리 정보 등
- 표준 헤더가 너무 많다.
- 필요 시, 임의의 헤더 추가가 가능하다. 단 약속한 클라이언트와 서버만이 해석할 수 있다.
  
## HTTP 메시지 바디
![http_msg_body](/assets/images/page/web/2022-01-04_http_msg_body.png)
- 실제 전송할 데이터를 포함한다.
- HTML 문서, 이미지, 영상, JSON 등 byte로 표현할 수 있는 모든 데이터를 전송할 수 있다.