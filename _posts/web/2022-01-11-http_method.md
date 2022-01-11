---
title: "HTTP 메서드"
excerpt: "HTTP 웹 기본 지식"
category: 
  - web
author_profile: true
sidebar:
  - nav: "main" 
tag:
  - http
  - get
  - post
  - put
  - patch
  - delete
toc: true
toc_sticky: true
---
> 이 포스트는 김영한님의 ['모든 개발자를 위한 HTTP 웹 기본 지식'](https://www.inflearn.com/course/http-%EC%9B%B9-%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%81%AC)을 수강하고 작성하였습니다.  

# HTTP 메서드
클라이언트가 서버에 요청을 할 때 기대하는 행동
- GET - 리소스 조회
- POST - 요청 데이터 처리, 주로 등록에 사용
- PUT - 리소스를 대체, 해당 리소스가 없으면 생성
- PATCH - 리소스 부분 변경
- DELETE - 리소스 삭제
- HEAD - GET과 동일하지만 메시지 부분을 제외하고 상태 줄과 헤더만 반환
- OPTIONS - 대상 리소스에 대한 통신 가능 옵션(메서드)을 설명(주로 CORS에서 사용)
- CONNECT - 대상 자원으로 식별되는 서버에 대한 터널을 설정
- TRACE - 대상 리소스에 대한 경로를 따라 메시지 루프백 테스트를 수행

최근 스펙에는 리소스가 Representation으로 변경됨. CONNECT와 TRACE는 거의 안 씀.

## GET
> ```
> GET /search?q=hello&hl=ko HTTP/1.1  
> HOST: www.google.com
> ```

- 리소스 조회
- 서버에 전달하고 싶은 데이터는 query(쿼리 파라미터, 쿼리 스트링)를 통해서 전달
- 메시지 바디를 이용해서 데이터를 전달할 수 있지만, 지원하지 않는 곳이 많아서 권장하지 않음

### 리소스 조회
![search1](/assets/images/page/web/2022-01-11-get1.jpg)

- 클라이언트가 members 100번의 정보를 요청하는 GET 메시지를 서버에 보낸다.
<br><br><br>

![search2](/assets/images/page/web/2022-01-11-get2.jpg)

- GET 메시지가 서버에 도착하면, 서버는 메시지를 해석한다.
- 서버는 데이터베이스를 조회하여 json 데이터를 생성한다.
<br><br><br>

![search3](/assets/images/page/web/2022-01-11-get3.jpg)

- 서버는 응답 메시지를 만들어서 클라이언트에 전송한다.
<br><br><br>

## POST
> ```
> POST /members HTTP/1.1  
> Content-Type: application/json
>
> {
>   "username": "hello",
>   "age": 20
> }
> ```

- 요청 데이터 처리
- **메시지 바디를 통해 서버로 요청 데이터 전달**
- 서버는 요청 데이터를 **처리**
  - 메시지 바디를 통해 들어온 데이터를 처리하는 모든 기능을 수행한다.
- 주로 전달된 데이터로 신규 리소스 등록, 프로세스 처리에 사용

### 리소스 등록
![post1](/assets/images/page/web/2022-01-11-post1.jpg)

- 요청을 '/members'에 전달한다. 이때 서버는 클라이언트로부터 '/members' 요청이 오면, 서버가 신규 등록 처리를 하도록 클라이언트와 서버끼리 약속이 되어 있는 상태이다.
<br><br><br>

![post2](/assets/images/page/web/2022-01-11-post2.jpg)

- 서버는 클라이언트로부터 받은 요청에 따라 데이터를 데이터베이스에 등록한다.
- 신규 리소스 식별자를 생성한다.
<br><br><br>

![post3](/assets/images/page/web/2022-01-11-post3.jpg)

- 리소스 등록 완료 메시지(201 Created, 200 메시지도 가능)를 보낸다.
   - 201로 보낼 때에는 Location으로 자원이 생성된 URI 경로를 보내준다.
<br><br><br>

### 요청 데이터 처리 예시
- 스펙 - POST 메서드는 **대상 리소스가 리소스의 고유한 의미 체계에 따라 요청에 포함된 표현을 처리하도록 요청**한다.
- 예시
  - HTML 양식에 입력된 필드와 같은 데이터 블록을 데이터 처리 프로세스에 제공
    - 예) HTML FORM에 입력한 정보로 회원 가입, 주문 등에서 사용
  - 게시판, 뉴스 그룹, 메일링 리스트, 블로그 또는 유사한 기사 그룹에 메시지 게시
    - 예) 게시판 글쓰기, 댓글 달기
  - 서버가 아직 식별하지 않은 새 리소스 생성
    - 예) 신규 주문 생성
  - 기존 자원에 데이터 추가
    - 예) 한 문서 끝에 내용 추가하기
- **정리 - 이 리소스 URI에 POST 요청이 오면 요청 데이터를 어떻게 처리할지 리소스마다 따로 정해야 함 = 정해진 것이 없음**

### 정리
POST는
1. **새 리소스 생성(등록)**
   - 서버가 아직 식별하지 않은 새 리소스 생성
2. **요청 데이터 처리**
   - 단순히 데이터를 생성하거나, 변경하는 것을 넘어서 프로세스를 처리해야 하는 경우
     - 예) 주문에서 결제완료 → 배달시작 → 배달완료 처럼 단순히 값 변경을 넘어 프로세스의 상태가 변경되는 경우
   - POST의 결과로 새로운 리소스가 생성되지 않을 수도 있음
     - **컨트롤 URI - 실무에서는 리소스만으로 URI를 설계할 수 없다. 이때 리소스의 동작에 해당하는 부분을 URI로 한다.**
       - 예) POST /orders/{orderId}/start-delivery
3. **다른 메서드로 처리하기 애매한 경우**
   - 예) JSON으로 조회 데이터를 넘겨야 하는데, GET 메서드를 사용하기 어려운 경우
   - 애매하면 POST

에 쓴다.

## PUT
> ```
> PUT /protoss/3 HTTP/1.1
> Content-Type: application/json
>
> {
>   "tribename": "purifier",
>   "population": 10000
> }
> ```

- 리소스를 대체
  - 리소스가 있으면 덮어쓰기
  - 리소스가 없으면 생성
- **클라이언트가 리소스를 식별**
  - 클라이언트가 리소스의 위치를 알고 URI를 지정한다는 점이 POST와의 차이

### 리소스가 있을 때의 PUT 처리
![put_with_resource1](/assets/images/page/web/2022-01-11-put_res1.jpg)

- 클라이언트가 members의 100번에 대한 PUT 요청을 서버에 보낸다.
<br><br><br>

![put_with_resource2](/assets/images/page/web/2022-01-11-put_res2.jpg)

- 서버에 이미 members의 100번 데이터가 있으면, 클라이언트로부터 받은 요청 데이터를 기존 데이터에 덮어씌운다.
<br><br><br>

### 리소스가 없을 때의 PUT 처리
![put_without_resource1](/assets/images/page/web/2022-01-11-put_no_res1.jpg)

- 클라이언트가 members의 100번에 대한 PUT 요청을 서버에 보낸다.
<br><br><br>

![put_without_resource2](/assets/images/page/web/2022-01-11-put_no_res2.jpg)

- 서버는 members의 100번에 대한 신규 리소스를 생성한다.
<br><br><br>

### ※ 리소스를 완전히 대체
![put_replace1](/assets/images/page/web/2022-01-11-put_replace1.jpg)

- 클라이언트가 members의 100번에 대한 PUT 요청을 서버에 보낸다. 이때 요청 메시지 내 /members/100의 필드에는 'username'이 없고, 서버의 /members/100 데이터에는 'username' 필드가 있다.
<br><br><br>

![put_replace2](/assets/images/page/web/2022-01-11-put_replace2.jpg)

- 서버는 PUT 요청에 따라 'username' 필드가 삭제된 형태로 기존의 /members/100의 데이터를 덮어씌운다.
<br><br><br>

## PATCH
> ```
> PATCH /members/100 HTTP/1.1
> Content-Type: application/json
>
> {
>   "age": 50
> }
> ```

- PUT과 다르게, 리소스를 부분 변경
- PATCH가 지원이 안 되는 서버의 경우, POST를 사용

### 리소스 부분 변경 처리
![patch1](/assets/images/page/web/2022-01-11-patch1.jpg)

- 클라이언트가 서버에 members의 100번 리소스의 'age'필드 값을 변경하는 PUT 요청을 보낸다. 이때 요청 메시지 내 /members/100의 필드에는 'username'이 없고, 서버의 /members/100 데이터에는 'username' 필드가 있다.
<br><br><br>

![patch2](/assets/images/page/web/2022-01-11-patch2.jpg)

- PUT과 다르게, 서버에 있는 /members/100의 필드 'username'은 그대로 두고, 'age' 필드의 값만 변경한다.
<br><br><br>

## DELETE
> ```
> DELETE /members/100 HTTP/1.1
> Host: localhost:8080
> ```

- 리소스 제거

### 리소스 제거 처리
![delete1](/assets/images/page/web/2022-01-11-delete1.jpg)

- 클라이언트가 서버에게 /members/100 리소스를 제거하는 DELETE 요청을 보낸다.
<br><br><br>

![delete2](/assets/images/page/web/2022-01-11-delete2.jpg)

- 서버는 /members/100 리소스를 제거한다.
<br><br><br>

# HTTP 메서드의 속성
- 안전 (Safe Methods)
- 멱등 (Idempotent Methods)
- 캐시가능(Cacheable Methods)

| HTTP 메서드 | RFC | 요청에 Body가 있음 | 응답에 Body가 있음 | 안전 | 멱등 | 캐시 가능 |
|:----------:|:---:|:-----------------:|:-----------------:|:----:|:----:|:--------:|
| GET | RFC 7231 | 아니오 | 예 | 예 | 예 | 예 |
| HEAD | RFC 7231 | 아니오 | 아니오 | 예 | 예 | 예 |
| POST | RFC 7231 | 예 | 예 | 아니오 | 아니오 | 예 |
| PUT | RFC 7231 | 예 | 예 | 아니오 | 예 | 아니오 |
| DELETE | RFC 7231 | 아니오 | 예 | 아니오 | 예 | 아니오 |
| CONNECT | RFC 7231 | 예 | 예 | 아니오 | 아니오 | 아니오 |
| OPTIONS | RFC 7231 | 선택 사항 | 예 | 예 | 예 | 아니오 |
| TRACE | RFC 7231 | 아니오 | 예 | 예 | 예 | 아니오 |
| PATCH | RFC 5789 | 예 | 예 | 아니오 | 아니오 | 예 |

＊ GET은 요청 메시지에 Body를 가질 수 있으나, 지원이 안 되는 곳도 있으므로 '요청에 Body가 있음' 항목에 '아니오'로 표시함

## 안전
- 호출해도 리소스를 변경하지 않는다.
  - Q. 그래도 계속 호출해서 로그 같은 게 쌓여서 장애가 발생하면?
    - A. 안전은 해당 리소스만 고려한다. 그런 부분까지 고려하지 않는다.

## 멱등
- f(f(x)) = f(x)
- 한 번 호출하든 두 번 호출하든 100번 호출하든 결과가 똑같다.
- 멱등 메서드
  - GET - 한 번 조회하든, 여러 번 조회하든 같은 결과가 조회된다.
  - PUT - 리소스를 대체한다. 따라서 같은 요청을 여러 번 해도 최종 결과는 같다.
  - DELETE - 리소스를 삭제한다. 같은 요청을 여러 번 해도 삭제된 결과는 똑같다.
- 멱등이 아닌 메서드
  - POST - 예시로 두 번 호출하면 같은 결제가 중복해서 발생할 수 있다.
- 활용
  - 자동 복구 메커니즘
    - 서버가 TIMEOUT 등으로 정상 응답을 못 주었을 때, 클라이언트가 같은 요청을 다시 해도 되는가의 판단 근거
- Q. 재요청 중간에 다른 곳에서 리소스를 변경해버리면?
  - A. 멱등은 외부 요인으로 중간에 리소스가 변경되는 것까지는 고려하지 않는다.

## 캐시가능
- 응답 결과 리소스를 캐시해서 사용해도 되는가?
  - 웹 브라우저가 내부에 리소스를 저장할 수 있는가?
- GET, HEAD, POST, PATCH 캐시 가능
- 실제로는 GET, HEAD 정도만 캐시로 사용
  - POST, PATCH는 본문 내용까지 캐시 키로 고려해야 하는데, 구현이 쉽지 않음
