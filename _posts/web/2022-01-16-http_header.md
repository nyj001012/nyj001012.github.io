---
title: "HTTP 헤더"
excerpt: "HTTP 웹 기본 지식"
category: 
  - web
author_profile: true
sidebar:
  - nav: "main" 
tag:
  - http
  - http header
toc: true
toc_sticky: true
last_modified_at: 2022-01-29T00:00:00+09:00
---
> 이 포스트는 김영한님의 ['모든 개발자를 위한 HTTP 웹 기본 지식'](https://www.inflearn.com/course/http-%EC%9B%B9-%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%81%AC)을 수강하고 작성하였습니다.  

# HTTP 헤더
- header-field: field-name ":" OWS field-value OWS (OWS: 띄어쓰기 허용)
- field-name은 대소문자 구분 없음
- HTTP 전송에 필요한 모든 부가정보
  - 예) 메시지 바디의 내용, 메시지 바디의 크기, 압축, 인증, 요청 클라이언트, 서버 정보, 캐시 관리 정보...
- 표준 헤더가 너무 많음
  - 참고: <https://en.wikipedia.org/wiki/List_of_HTTP_header_fields>
- 필요 시 임의의 헤더 추가 가능

# RFC2616 (폐기됨)
## HTTP HEADER
![RFC2616_header](/assets/images/page/web/2022-01-16_rfc2616_header.png)
- General 헤더: 메시지 전체에 적용되는 정보
  - 예) Connection: close
- Request 헤더: 요청 정보
  - 예) User-Agent: Mozilla/5.0 (Macintosh; ..)
- Response 헤더: 응답 정보
  - 예) Server: Apache
- Entity 헤더: 엔티티 바디 정보
  - 예) Content-Type: text/html, Content-Length: 3423

## HTTP BODY
### message body - RFC2616
![RFC2616_message_body](/assets/images/page/web/2022-01-16_rfc2616_msgbody.jpg)
- 메시지 본문(message body)은 엔티티 본문(entity body)을 전달하는 데 사용
- 엔티티 본문은 요청이나 응답에서 전달할 실제 데이터
- **엔티티 헤더**는 **엔티티 본문**의 데이터를 해석할 수 있는 정보 제공
  - 데이터 유형(html, json), 데이터 길이, 압축 정보 등등

# RFC723×
- 엔티티(Entity) → 표현(Representation)
- 표현(Representation) = 표현 메타데이터(Representation Metadata) + 표현 데이터(Representation Data)

## HTTP BODY
### message body - RFC7230(최신)
![RFC7230_message_body](/assets/images/page/web/2022-01-16_rfc7230_msgbody.jpg)
- 메시지 본문(message body)을 통해 표현 데이터 전달
- 메시지 본문 = 페이로드(payload)
- **표현**은 요청이나 응답에서 전달할 실제 데이터
  - 리소스가 html, json 등으로 표현될 수 있기 때문에 이름을 저렇게 지었다고 함
- **표현 헤더**는 **표현 데이터**를 해석할 수 있는 정보 제공
  - 데이터 유형(html, json), 데이터 길이, 압축 정보 등등
- 참고: 표현 헤더는 표현 메타데이터와, 페이로드 메시지를 구분해야 하지만, 여기서는 생략

# 표현
![representation](/assets/images/page/web/2022-01-16_representation.jpg)
- Content-Type: 표현 데이터의 형식
- Content-Encoding: 표현 데이터의 압축 방식
- Content-Language: 표현 데이터의 자연 언어
- Content-Length: 표현 데이터의 길이

- 표현 헤더는 전송, 응답 둘 다 사용

## Content-Type
![content-type](/assets/images/page/web/2022-01-16_rep_cont_type.jpg)
- 표현 데이터의 형식 설명
- 미디어 타입, 문자 인코딩
- 예)
  - text/html; charset=utf-8
  - application/json (json은 기본적으로 charset=utf-8)
  - image/png

## Content-Encoding
![content-encoding](/assets/images/page/web/2022-01-16_rep_cont_enc.jpg)
- 표현 데이터 인코딩
- 표현 데이터를 압축하기 위해 사용
- 데이터를 전달하는 곳에서 압축 후 인코딩 헤더 추가
- 데이터를 읽는 쪽에서 인코딩 헤더의 정보로 압축 해제
- 예)
  - [gzip](https://ko.wikipedia.org/wiki/Gzip): 압축
  - [deflate](https://ko.wikipedia.org/wiki/DEFLATE): 압축
  - identity: 압축 안 함

## Content-Language
![content-language](/assets/images/page/web/2022-01-16_rep_cont_lang.jpg)
- 표현 데이터의 자연 언어를 표현
- 예)
  - ko
  - en
  - en-US

## Content-Length
![content-length](/assets/images/page/web/2022-01-16_rep_cont_length.jpg)
- 표현 데이터의 길이
- 바이트 단위
- Transfer-Encoding(분할 전송)을 사용하면 Content-Length를 사용하면 안 됨

# 협상 (Content negotiation)
- 클라이언트가 선호하는 표현 요청
- Accept: 클라이언트가 선호하는 미디어 타입 전달
- Accept-Charset: 클라이언트가 선호하는 문자 인코딩
- Accept-Encoding: 클라이언트가 선호하는 압축 인코딩
- Accept-Language: 클라이언트가 선호하는 자연 언어

- 협상 헤더는 요청 시에만 사용

## 협상과 우선순위
### Quality Values(q)
- Quality Values(q) 값 사용
- 0~1, **클수록 높은 우선순위**
- 1은 생략 가능
- 예) Accept-Language: ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7
  1. ko-KR;q=1 (q 생략)
  2. ko;q=0.9
  3. en-US;q=0.8
  4. en;q=0.7

- 구체적인 것을 우선한다.
- 예) Accept: **text/\***, **text/plain**, **text/plain;format=flowed**, **\*/\***
  1. text/plain;format=flowed
  2. text/plain
  3. text/*
  4. */*

- 구체적인 것을 기준으로 미디어 타입을 맞춘다.
- 예) Accept: **text/\***;q=0.3, **text/html**;q=0.7, **text/html;level=1**, **text/html;level=2**;q=0.4, **\*/\***;q=0.5  

  | Media Type | Quality |
  |------------|:-------:|
  | text/html;level=1 | 1 |
  | text/html | 0.7 |
  | text/plain | 0.3 |
  | image/jpeg | 0.5 |
  | text/html;level=2 | 0.4 |
  | text/html;level=3 | 0.7 |

## 예시: Accept-Language
### Accept-Language 적용 전
![without_accept-language](/assets/images/page/web/2022-01-16_wo_cn.jpg)
1. 클라이언트가 서버로 '/event' 리소스를 요청하는데, 아무런 추가 정보(한국어 지원 등)이 없다.
2. 서버는 기본값인 영어로 브라우저에 응답한다.
3. '/event' 페이지에 접속하면 컨텐츠들이 전부 영어로 표시된다.

### Accept-Language 적용 후
![with_accept-language1](/assets/images/page/web/2022-01-16_w_cn1.jpg)
1. 클라이언트가 서버로 '/event' 리소스를 요청하는데, 선호하는 언어가 한국어임을 같이 요청한다.
2. 서버는 `Content-Language`를 한국어로 하여 메시지 바디를 구성하고 응답한다.
3. '/event' 페이지에 접속하면 컨텐츠들이 전부 한국어로 표시된다.

![with_accept-language2](/assets/images/page/web/2022-01-16_w_cn2.jpg)
1. 클라이언트가 서버로 '/event' 리소스를 요청하는데, 선호하는 언어가 한국어임을 같이 요청한다.
2. 서버는 지원 언어 중에 독일어(기본), 영어 밖에 없으므로, 기본 언어인 독일어로 응답한다.
3. '/event' 페이지에 접속하면 컨텐츠들이 전부 독일어로 표시된다.

![with-accept-language3](/assets/images/page/web/2022-01-16_w_cn3.jpg)
1. 클라이언트가 서버로 '/event' 리소스를 요청하는데, 선호하는 언어 우선순위와 같이 요청한다.
2. 서버는 `Accept-Language`의 우선순위를 고려하여, 영어로 메시지바디를 구성하고 응답한다.
3. '/event' 페이지에 접속하면 컨텐츠들이 전부 영어로 표시된다.

# 전송 방식
## 단순 전송
![simple_transfer](/assets/images/page/web/2022-01-16_simple_trans.jpg)
- message body의 `Content-Length`를 지정한다. 즉, 컨텐츠의 길이를 알 때 쓸 수 있다.
- 한 번에 전부 전송하고, 한 번에 전부 받는다.

## 압축 전송
![compact_transfer](/assets/images/page/web/2022-01-16_compact_trans.jpg)
- 서버에서 message body를 압축한다.
- `Content-Encoding`을 지정함으로써 어떤 방식으로 압축했는지 알려준다.

## 분할 전송
![chunked_transfer](/assets/images/page/web/2022-01-16_chunk_trans.jpg)
- message body를 바이트 단위로 쪼개서 전송한다.
  - 예)
    1. 서버가 5byte Hello를 보낸다.
    2. 클라이언트가 5byte Hello를 받는다.
    3. 서버가 5byte World를 보낸다.
    4. 클라이언트가 5byte World를 받는다.
    5. 서버가 전송이 끝났음을 알리는 0byte \r\n을 보낸다.
- 용량이 큰 내용을 보낼 때 사용한다.
- Content-Length를 지정하면 안 된다.
  - chunk 마다의 길이가 있다보니, Content-Length가 예측이 안 된다.

## 범위 전송
![range_transfer](/assets/images/page/web/2022-01-16_range_trans.jpg)
- 클라이언트가 서버로 `Range` 범위에 속한 message body의 내용을 요청한다.
- 서버는 `Content-Range: Range / message body의 총 길이`를 지정하고, `Range` 범위 내의 message body 내용을 응답한다.

# 일반 정보
- From: 유저 에이전트의 이메일 정보
- Referer: 이전 웹 페이지 주소
- User-Agent: 유저 에이전트 어플리케이션 정보
- Server: 요청을 처리하는 ORIGIN 서버의 소프트웨어 정보
- Date: 메시지가 생성된 날짜

## From
- 유저 에이전트의 이메일 정보
- 일반적으로 잘 사용되지 않음
- 검색 엔진 같은 곳에서 주로 사용
- 요청에서 사용

## Referer ★
- 현재 요청된 페이지의 이전 웹 페이지 주소
- A → B로 이동하는 경우, B를 요청할 때 Referer: A를 포함해서 요청
- Referer를 사용해서 유입 경로 분석 가능
- 요청에서 사용

(referer는 단어 referrer의 오타인데, 이미 많은 HTTP에서 referer로 사용하고 있어서 고치기 힘들기 때문에 그냥 쓴다고 한다.)

## User-Agent
- 클라이언트의 어플리케이션(유저 에이전트) 정보(웹 브라우저 정보 등)
  - 예) Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36
- 통계 정보
- 어떤 종류의 브라우저에서 장애가 발생하는지 파악 가능
- 요청에서 사용

## Server
- 요청을 처리하는 ORIGIN 서버의 소프트웨어 정보
  - ORIGIN 서버: HTTP 요청은 수많은 프록시 서버들을 거치는데, 맨 처음 요청을 보냈고, 응답을 최종적으로 받는 서버
- Server: Apache/2.2.22 (Debian)
- server: nginx
- 응답에서 사용

## Date
- 메시지가 발생한 날짜와 시간
- Date: Tue, 15 Nov 1994 08:12:31 GMT
- 과거에는 요청에서도 사용했으나, 최신 스펙에서는 응답에서만 사용

# 특별한 정보
- Host: 요청한 호스트 정보(도메인)
- Location: 페이지 리다이렉션
- Allow: 허용 가능한 HTTP 메서드
- Retry-After: 유저 에이전트가 다음 요청을 하기까지 기다려야 하는 시간

## Host
> GET /serch?q=hello&hl=ko HTTP/1.1  
> Host: www.google.com

- 요청에서 사용
- 필수 값
- 하나의 서버가 여러 도메인을 처리해야 할 때  
- 하나의 IP 주소에 여러 도메인이 적용되어 있을 때
  - 서버가 가상 호스트를 통해 도메인을 한 번에 처리할 수 있는데, 이때 실제 어플리케이션이 여러 개 구동될 수 있다.

![host](/assets/images/page/web/2022-01-16_virtual_host.jpg)
1. 클라이언트는 200.200.200.2 서버에 /hello 리소스를 요청한다. 
2. 서버는 'aaa.com'에 대한 요청인지, 'bbb.com'에 대한 요청인지, 'ccc.com'에 대한 요청인지를 요청 메시지의 `Host`를 통해 구분한다.

## Location
- 페이지 리다이렉션
- 웹 브라우저는 3×× 응답의 결과에 Location 헤더가 있으면, Location 위치로 자동 이동(리다이렉트)
- 201 (Created): Location 값은 요청에 의해 생성된 리소스 URI
- 3×× (Redirection): Location 값은 요청을 자동으로 리다이렉션하기 위한 대상 리소스를 가리킴

## Allow
- 허용 가능한 HTTP 메서드
- 405 (Method Not Allowed) 에서 응답에 포함해야 함
  - 예) Allow: GET, HEAD, PUT
- 사실 서버에서 많이 구현하지는 않는다고 한다.

## Retry-After
- 유저 에이전트가 다음 요청을 하기까지 기다려야 하는 시간
- 503 (Service Unavailable): 서비스가 언제까지 불능인지 알려줄 수 있음
- Retry-After: Fri, 31 Dec 1999 23:59:59 GMT (날짜 표기)
- Retry-After: 120 (초 단위 표기)

# 인증
- Authorization: 클라이언트 인증 정보를 서버에 전달
- WWW-Authenticate: 리소스 접근 시 필요한 인증 방법 정의

## Authorization
- 클라이언트 인증 정보를 서버에 전달
  - 예) Authorization: Basic xxxxxxxxxxxxx
- 인증 메커니즘에 따라 값이 달라짐
- HTTP에서는 일단 인증 메커니즘에 상관 없이 Authorization 헤더 제공

## WWW-Authenticate
- 리소스 접근 시 필요한 인증 방법 정의
- 401 Unauthorized 응답과 함께 사용
  - 예) WWW-Authenticate: Newauth realm="apps", type=1, title="Login to \"apps\"", Basic realm="simple"

# 쿠키 ★
- Set-Cookie: 서버에서 클라이언트로 쿠키 전달(응답)
  - 예) set-cookie: **sessionId=mokoko**; **expires**=Sat, 17-Jen-2022 00:00:00 GMT; **path**=/; **domain**=.google.com; **Secure**
- Cookie: 클라이언트가 서버에서 받은 쿠키를 저장하고, HTTP 요청 시 서버로 전달
- 사용처
  - 사용자 로그인 세션 관리
  - 광고 정보 트래킹
- 쿠키 정보는 항상 서버에 전송됨
  - 네트워크 트래픽 추가 유발
  - 최소한의 정보만 사용(세션 id, 인증 토큰)
  - 서버에 전송하지 않고, 웹 브라우저 내부에 데이터를 저장하고 싶으면 웹 스토리지(localStorage, sessionStorage) 참고
- 주의할 점
  - **보안에 민감한 데이터는 저장하면 안 됨(주민번호, 신용카드 번호 등등)**

## 쿠키 등장 배경
- HTTP는 무상태 프로토콜이기 때문에, 클라이언트와 서버는 서로 상태를 유지하지 않는다. 즉 클라이언트와 서버가 요청과 응답을 주고받으면 연결이 끊어진다.
- 클라이언트가 요청을 다시 해도 서버는 이전 요청을 기억하지 못 한다.
  - 예) 로그인 이후 다른 페이지에 접근하면, 내 로그인 정보가 사라진다.
- 대안으로 모든 요청과 링크에 사용자 정보를 포함할 수 있겠지만, 보안 상으로나 개발 상의 문제가 있다.

## 쿠키 예시 - 로그인
![cookie1](/assets/images/page/web/2022-01-16_cookie1.jpg)
- 웹 브라우저에서 POST로 로그인을 한다.
- 서버는 `Set-Cookie`를 통해 `user=홍길동`을 지정하고 응답한다.
- 웹 브라우저 내의 쿠키 저장소에 `user=홍길동`을 저장한다.
  - 실제로는 `user=홍길동`으로 바로 저장하기엔 보안 상 위험하므로, 서버에서 session key를 만들어서 서버의 데이터베이스에 저장하고 그 값을 이용한다고 한다(`sessionId=session key`).

![cookie2](/assets/images/page/web/2022-01-16_cookie2.jpg)
- 웹 브라우저가 '/welcome' 페이지에 접근한다.
- 웹 브라우저는 쿠키 저장소의 `user=홍길동`을 가져와서 HTTP 헤더에 `Cookie: user=홍길동`을 추가한다.
- 클라이언트의 요청이 서버에 도착하면, 쿠키의 내용을 보고 응답한다.

![cookie3](/assets/images/page/web/2022-01-16_cookie3.jpg)
- 쿠키는 모든 요청에 쿠키 정보를 자동으로 포함한다.

## 쿠키 생명주기
- expires: 만료일이 되면 쿠키 삭제
  - 예) Set-Cookie: **expires**=Sat, 17-Jen-2022 00:00:00 GMT;
- max-age: 0이나 음수를 지정하면 쿠키 삭제
  - 예) Set-Cookie: **max-age**=3600 (3600초)
- 세션 쿠키: 만료 날짜를 생략하면 브라우저 종료 시까지만 유지
- 영속 쿠키: 만료 날짜를 입력하면 해당 날짜까지 유지

## 쿠키 접근 설정
### 도메인 이용
- 쿠키가 생성되는 도메인을 지정
- **명시: 명시한 문서 기준 도메인 + 서브 도메인**
  - 예) domain=example.org를 지정해서 쿠키 생성하면 example.org와 dev.example.org도 쿠키 접근(쿠키를 같이 전송)
- **생략: 현재 문서 기준 도메인만 적용**
  - 예) example.org에서 쿠키를 생성하고 domain 지정을 생략하면 example.org에서만 쿠키 접근

### 경로 이용
- 쿠키 접근 경로를 지정
  - 예) path=/home
- **이 경로를 포함한 하위 경로 페이지만 쿠키 접근**
- **일반적으로 path=/ 루트로 지정**
  - 예) **path=/home 지정**
    - /home 쿠키 접근 가능
    - /home/level1 쿠키 접근 가능
    - /home/level1/level2 쿠키 접근 가능
    - /hello 쿠키 접근 불가능

## 쿠키 보안
### Secure
- 쿠키는 http, https를 구분하지 않고 전송
- Secure를 적용하면 https인 경우에만 전송

### HttpOnly
- XSS 공격 방지
- 자바스크립트에서 접근 불가(document.cookie 불가)
- HTTP 전송에만 사용

### SameSite
- XSRF 공격 방지
- 요청 도메인과 쿠키에 설정된 도메인이 같은 경우에만 쿠키 전송

# 캐시 기본 동작
## 캐시가 없다면
- 데이터가 변경되지 않아도 계속 네트워크를 통해서 요청 때마다 데이터를 다운로드 받아야 한다.
- 인터넷 네트워크는 매우 느리고 비싸다.
- 브라우저 로딩 속도가 느리다.
- 느린 사용자 경험

## 캐시
- 캐시 가능 시간 동안 네트워크를 사용하지 않아도 된다.
- 비싼 네트워크 사용량을 줄일 수 있다.
- 브라우저 로딩 속도가 매우 빠르다.
- 빠른 사용자 경험

### 캐시 적용 예시
![with_cache1](/assets/images/page/web/2022-01-29_w_cache1.jpg)

- 웹 브라우저에서 서버로 '/star.jpg' 리소스를 GET으로 요청한다.
- 서버는 HTTP 헤더에 `cache-control`(캐시 유효 시간, 초 단위)을 추가한 응답 메시지를 웹 브라우저로 전송한다.

![with_cache2](/assets/images/page/web/2022-01-29_w_cache2.jpg)

- 웹 브라우저 내의 캐시 저장소에 응답 결과를 저장한다.

![with_cache3](/assets/images/page/web/2022-01-29_w_cache3.jpg)

- 웹 브라우저가 똑같은 리소스를 60초 내로 요청한다.

![with_cache4](/assets/images/page/web/2022-01-29_w_cache4.jpg)

- 웹 브라우저가 요청한 리소스를 서버가 아니라, 캐시 저장소에서 응답한다.

# 검증 헤더와 조건부 요청
- 캐시 유효 시간을 초과해도 서버의 데이터가 갱신되지 않으면 304 Not Modified, 헤더 메타 정보만 응답
- 클라이언트는 서버가 보낸 응답 헤더 정보로 캐시의 메타 정보를 갱신
- 클라이언트는 캐시에 저장되어 있는 데이터 재활용
- 결과적으로 네트워크 다운로드가 발생하더라도 용량이 작은 헤더 정보만 다운로드

## 검증 헤더
- 캐시 데이터와 서버 데이터가 같은지 검증하는 데이터
  - 예) 
    - Last-Modified: Thu, 04 Jun 2020 07:19:24 GMT 
    - ETag: "v1.0"

## 조건부 요청 헤더
- 검증 헤더로 조건에 따른 분기
- If-Modified-Since 또는 If-Unmodified-Since와 Last-Modified 사용
- If-None-Match 또는 If-Match와 ETag 사용
- 조건을 만족하면 200 OK
- 조건을 만족하지 않으면 304 Not Modified

## 검증 헤더와 조건부 요청 등장 배경
- 캐시 유효 시간을 초과하여 서버에 다시 요청하면 고려해야 할 상황
  - 서버에서 기존 데이터를 변경
  - 서버에서 기존 데이터를 변경하지 않음
    - 같은 데이터인데 굳이 다시 다운로드 받을 필요가 있을까?
    - 서버에서 데이터를 전송하는 대신에 저장해 둔 캐시를 재사용 할 수 있다.
    - 단, 클라이언트의 데이터와 서버의 데이터가 같다는 사실을 확인해야 한다.

## If-Modified-Since, Last-Modified
![ims_lm1](/assets/images/page/web/2022-01-29_ims_lm1.jpg)

- 웹 브라우저에서 서버로 '/star.jpg' 리소스를 GET으로 요청한다.
- 서버는 HTTP 응답 메시지에 데이터가 마지막으로 수정된 시간인 `Last-Modified`(UTC 표기) 값을 포함하여 웹 브라우저로 전송한다.

![ims_lm2](/assets/images/page/web/2022-01-29_ims_lm2.jpg)

- 데이터 최종 수정일을 포함한 응답 결과를 캐시에 저장한다.

![ims_lm3](/assets/images/page/web/2022-01-29_ims_lm3.jpg)

- 캐시 유효 시간이 지나고 다시 서버에 요청을 보내면, 캐시 저장소 내의 리소스를 사용할 수 없다.
- 웹 브라우저는 캐시 내의 리소스에 `Last-Modified` 값이 있음을 알고 있다. 따라서 서버에게 캐시가 가지고 있는 데이터 최종 수정일인 `if-modified-since` 값이 추가된 요청 메시지를 전송한다.
- 서버는 `if-modified-since` 값과 서버 내 리소스의 데이터 최종 수정일을 비교한다.

![ims_lm4](/assets/images/page/web/2022-01-29_ims_lm4.jpg)

- `if-modified-since` 값과 서버 내 리소스의 데이터 최종 수정일이 같다면, `304 Not Modified` 응답을 한다. 이때 HTTP Body는 없다. '/star.jpg'의 용량은 1.1M임에 반해, 0.1M의 HTTP 메시지만 전송한다.
- 브라우저 캐시 내의 `cache-control`과 `Last-Modified` 값을 갱신한다.
- 이후 웹 브라우저는 갱신된 캐시를 사용한다.

### If-Modified-Since, Last-Modified 단점
- 1초 미만(0.×초) 단위로 캐시 조정 불가능
- 날짜 기반의 로직 사용
- 데이터를 수정해서 날짜가 다르지만, 같은 데이터를 수정해서 데이터 결과가 똑같아도 다시 다운로드
- 서버에서 별도의 캐시 로직을 관리하고 싶은 경우 어떻게 할 것인가?
  - 예) 스페이스나 주석처럼 크게 영향이 없는 변경에서 캐시를 유지하고 싶을 때

## ETag(Entity Tag), If-None-Match
- 캐시용 데이터에 임의의 고유한 버전 이름을 사용
  - 예) ETag: "v1.0", ETag: "probe1"
- 데이터가 변경되면 이 이름을 바꾸어서 변경(Hash 재생성)
  - 데이터가 같으면 Hash 값은 같지만, 데이터가 다르면 Hash 값이 다르게 나옴
- 클라이언트는 ETag만 보내서 같으면 유지, 다르면 다시 받으면 됨
- **캐시 제어 로직을 서버에서 완전히 관리**
- 클라이언트는 ETag 값을 서버에 제공, 클라이언트는 캐시 메커니즘을 모르는 상태
- 예)
  - 서버는 베타 오픈 기간인 3일 동안 파일이 변경되어도 ETag를 동일하게 유지
  - 어플리케이션 배포 주기에 맞춰 ETag 모두 갱신

![et_inm1](/assets/images/page/web/2022-01-29_et_inm1.jpg)

- 웹 브라우저에서 서버로 '/star.jpg' 리소스를 GET으로 요청한다.
- 서버는 HTTP 응답 메시지에 '/star.jpg'의 해시 값인 `ETag` 값을 포함하여 웹 브라우저로 전송한다.
- 캐시 저장소에는 `ETag` 값이 포함된 응답 결과를 저장한다.

![et_inm2](/assets/images/page/web/2022-01-29_et_inm2.jpg)

- 웹 브라우저가 캐시 유효 시간을 초과하여 서버로 요청 메시지를 보낼 때, 캐시 저장소 내 '/star.jpg'의 `ETag` 값을 `If-None-Match`의 값으로 지정하여 요청 메시지를 보낸다.
- 데이터가 수정되지 않았으므로, 서버는 `304 Not Modified` 응답을 한다. 이때 HTTP Body는 없다.
- 캐시 저장소 내 '/star.jpg'의 캐시를 갱신한다.
- 이후 웹 브라우저는 갱신된 캐시를 사용한다.

# 캐시와 조건부 요청 헤더
- Cache-Control: 캐시 제어
- Pragma: 캐시 제어(하위 호환)
- Expires: 캐시 유효 기간

## Cache-Control
- Cache-Control: max-age 
  - 캐시 유효 시간, 초 단위
- Cache-Control: no-cache
  - 데이터는 캐시해도 되지만, 항상 origin 서버에 검증하고 사용
- Cache-Control: no-store 
  - 데이터에 민감한 정보가 있으므로 저장하면 안 됨(메모리에서 사용하고 최대한 빨리 삭제)
- Cache-Control: must-revalidate
  - 캐시 만료 후 최초 조회 시, origin 서버에 검증해야 함
  - origin 서버 접근 실패 시, 반드시 오류가 발생해야 함, 504(Gateway Timeout)
  - must-revalidate는 캐시 유효 시간 내라면 캐시를 사용
- Cache-Control: public 
  - 응답이 public 캐시(프록시 캐시 서버)에 저장되어도 됨
- Cache-Control: private 
  - 응답이 해당 사용자만을 위한 것, private 캐시(웹 브라우저 캐시)에 저장해야 함(기본값)
- Cache-Control: s-maxage 
  - 프록시 캐시에만 적용되는 max-age
- Age: 60 (HTTP 헤더) 
  - origin 서버에서 응답 후 프록시 캐시 내에 머문 시간(초 단위)

### Cache-Control: no-cache 동작
![no-cache1](/assets/images/page/web/2022-01-29_no_cache1.jpg)

- 웹 브라우저가 프록시 캐시 서버에 `no-cache`와 `ETag`를 이용하여 요청한다.
- 프록시 캐시 서버는 `no-cache`에 의해 원 서버에 요청한다.
- 원 서버는 검증을 하고 프록시 캐시 서버에 응답을 한다.
- 프록시 캐시 서버는 웹 브라우저에 응답하고, 결과가 브라우저 캐시에 저장된다.
- 웹 브라우저는 브라우저 캐시의 데이터를 사용한다.

## Pragma
- Pragma: no-cache 
  - Cache-Control: no-cache와 같은 역할
- HTTP 1.0 하위 호환으로, 지금은 사용하지 않는 편

## Expires
- 캐시 만료일을 정확한 날짜로 지정
  - 예) expires: Mon, 01 Jan 1990 00:00:00 GMT
- HTTP 1.0부터 사용
- 지금은 더 유연한 Cache-Control: max-age 권장
- Cache-Control: max-age와 함께 사용하면 Expires는 무시

# 프록시 캐시
![proxy_cache](/assets/images/page/web/2022-01-29_proxy_cache.jpg)

- 웹 브라우저가 프록시 캐시 서버에 접근하여 요청한다. 이때 웹 브라우저는 DNS 등을 확인하여 원(origin) 서버가 아니라 프록시 캐시 서버에 요청하도록 되어있음을 인지한 상태이다.
- 프록시 캐시 서버가 웹 브라우저에 응답하는데(public 캐시를 응답), 이는 미국에 있는 원 서버보다 응답 속도가 빠르다.

# 캐시 무효화
- 캐시를 적용하지 않아도 GET 요청의 경우에는 웹 브라우저가 임의로 캐시를 하기도 한다.
- 캐시 방지를 확실하게 하기 위한 캐시 무효화 응답
  - **Cache-Control: no-cache, no-store, must-revalidate**
  - **Pragma: no-cache**

## no-cache와 must-revalidate를 왜 같이 써야할까?
- 순간 네트워크 단절 등의 이유로 origin 서버에 접근이 불가능해지면
  - no-cache는 캐시 서버 설정에 따라 캐시 데이터를 반환할 수 있다. 즉, 브라우저 캐시 내의 오래된 데이터라도 반환할 수 있다.
    - Error or 200 OK
  - must-revalidate는 항상 오류가 발생해야 한다.
    - 504 Gateway Timeout
