---
title: "PORT"
excerpt: "HTTP 웹 기본 지식"
category: 
  - web
author_profile: true
sidebar:
  - nav: "main" 
tag:
  - http
  - port
---
> 이 포스트는 김영한님의 ["모든 개발자를 위한 HTTP 웹 기본 지식"](https://www.inflearn.com/course/http-%EC%9B%B9-%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%81%AC)을 수강하고 작성하였습니다.  

## PORT
![PORT](/assets/images/page/web/2021-12-17_port.png)
1. 포트는 같은 IP 내에서 프로세스를 구분하기 위한 것이다.  
즉, IP가 100.100.100.1인 클라이언트에서 게임, 화상통화, 웹 브라우저 중에 어떤 프로세스가 200.200.200.2, 200.200.200.3인 서버와 연결하고 싶어하는지를 구분할 수 있다.  
이 그림에서는 200.200.200.2:11220과 게임 100.100.100.1:8090, 200.200.200.2:32202와 화상통화 100.100.100.1:21000이 연결되어 있고, 200.200.200.3:80에 요청을 보내는 건 100.100.100.1:10010이다.  
2. 0~65,535의 범위 내에서 할당이 가능하다.
   1. 왜 port 번호의 범위가 0~65,535일까?
      1. port 번호는 일반적으로 unsigned short의 2바이트 정수형을 사용하는데, 이 데이터 타입이 표현할 수 있는 값의 범위가 0~65,535이다.  
3. 0~1023은 잘 알려진 포트로, 사용하지 않는 것이 좋다.
   1. FTP: 20, 21
   2. TELNET: 23
   3. HTTP: 80
   4. HTTPS: 443

## PORT 정보는 어디에?
![Port_in_packet](/assets/images/page/web/2021-12-17_tcpip_packet.png)
1. port는 TCP/IP 패킷에서 TCP 세그먼트에, 그리고 UDP에도 정보가 들어있다.