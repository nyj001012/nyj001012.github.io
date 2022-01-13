---
title: "HTTP 메서드 활용"
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

# 클라이언트에서 서버로 데이터 전송
- 쿼리 파라미터를 통한 데이터 전송
  - GET
    - 주로 정렬 필터(검색어)
- 메시지 바디를 통한 데이터 전송
  - POST, PUT, PATCH
    - 회원 가입, 상품 주문, 리소스 등록, 리소스 변경

## 정적 데이터 조회
![static](/assets/images/page/web/2022-01-12-static_get.jpg)

- 이미지, 정적 텍스트 문서
- 조회는 GET 사용
- 정적 데이터는 일반적으로 쿼리 파라미터 없이 리소스 경로로 단순하게 조회 가능


## 동적 데이터 조회
![dynamic](/assets/images/page/web/2022-01-12-dynamic_get.jpg)

- 주로 검색, 게시판 목록에서 정렬 필터(검색어)
- 조회 조건을 줄여주는 필터, 조회 결과를 정렬하는 정렬 조건에 주로 사용
- 조회는 GET 사용
- GET은 쿼리 파라미터 사용해서 데이터를 전달

## HTML Form을 통한 데이터 전송
- **HTML Form 전송은 GET, POST만 지원한다.**

### HTML Form submit시 POST 전송
![form_post](/assets/images/page/web/2022-01-12-form_post.jpg)
- `<input name>`의 값을 key, `<input>`의 값을 value로 하는 쿼리 파라미터 형식으로 데이터를 만들어 HTTP body에 넣는다.
- 데이터에 한글과 같은 문자가 포함되어 있으면, 인코딩되기 때문에 `urlencoded`가 `Content-Type`으로 지정됐다.
- 사용 예) 회원 가입, 상품 주문, 데이터 변경

### Content-Type: application/x-www-form-urlencoded 사용
- form의 내용을 메시지 바디를 통해서 전송한다(key=value, 쿼리 파라미터 형식).
- 전송 데이터를 url encoding 처리한다.
  - 예) abc김 → abc%EA%B9%80

### HTML Form - GET
![form_get1](/assets/images/page/web/2022-01-12-form_get1.jpg)
- HTTP method 부분이 GET으로 지정된다.
- 메시지 바디를 쓰지 않으므로, 쿼리로 데이터를 전송한다.
(추가적으로 학교에서는 저렇게 하면 정보 유출의 가능성이 있어서, GET 방식으로는 조회 이외의 목적으로 데이터를 전달하지 말라고 배웠다.)

![form_get2](/assets/images/page/web/2022-01-12-form_get2.jpg)
- username이 kim이고 age가 20인 데이터를 조회하는 필터링 목적의 GET 전송이다.
- 사용 예) 검색, 필터

### Content-Type: multipart/form-data
![form_multipart](/assets/images/page/web/2022-01-12-form_multipart.jpg)
- 파일 업로드 같은 binary 데이터를 전송할 때 사용한다.
- 다른 종류의 여러 파일과 폼의 내용을 함께 전송할 수 있다.


## HTTP API를 통한 데이터 전송
![http_api_transmit](/assets/images/page/web/2022-01-12-http_api_transmit.jpg)

- 서버 to 서버
  - 백엔드 시스템 통신
- 앱 클라이언트
  - 아이폰, 안드로이드
- 웹 클라이언트
  - HTML에서 Form 전송 대신 자바 스크립트를 통한 통신에 사용(AJAX)
    - 예) React, Vue.js 같은 웹 클라이언트와 API 통신
- POST, PUT, PATCH: 메시지 바디를 통해 데이터 전송
- GET: 조회, 쿼리 파라미터로 데이터 전달
- Content-Type: application/json을 주로 사용 (사실상 표준)
  - 종류: TEXT, XML, JSON 등
- 사용 예) 회원 가입, 상품 주문, 데이터 변경

# HTTP API 설계
## 컬렉션
- **[POST 기반 등록](#post---신규-자원-등록-특징)**
  - 예) 회원 관리 API 제공
- 서버가 관리하는 리소스 디렉토리
- **서버가 리소스의 URI를 생성하고 관리**

## 스토어
- **[PUT 기반 등록](#put---신규-자원-등록-특징)**
  - 예) 정적 컨텐츠 관리, 원격 파일 관리
- 클라이언트가 관리하는 리소스 저장소
- **클라이언트가 리소스의 URI를 알고 관리**

## HTML FORM 사용
- HTML FORM은 GET, POST만 지원, 따라서 제약이 있음
- AJAX 같은 기술을 사용해서 위의 문제 해결 가능
- **[컨트롤 URI](#컨트롤-uri)** 사용

## POST 기반, PUT 기반 차이
### POST - 신규 자원 등록 특징
- 클라이언트는 등록될 리소스의 URI를 모른다.
  - 회원 등록 /members → POST
  - POST /members
- 서버가 새로 등록된 리소스 URI를 생성해준다.  
  > ```
  > HTTP/1.1 201 Created  
  > Location: /members/100
  > ```
- 예시로 회원 관리 시스템에서 컬렉션은 /members
- 대부분 POST 기반을 많이 사용한다.

### PUT - 신규 자원 등록 특징
- 클라이언트가 리소스 URI를 알고 있어야 한다.
  - 파일 등록 /files/{filename} → PUT
  - PUT /files/star.jpg
- 클라이언트가 직접 리소스의 URI를 지정한다.
- 예시로 파일 관리 시스템에서 스토어는 /files

## 컨트롤 URI
> 최대한 리소스로 URI를 설계하고 그래도 안 되면 컨트롤 URI를 쓰자.

- HTML FORM의 제약을 해결하기 위해 동사로 된 리소스 경로를 사용한다.
- HTTP API를 포함한 HTTP 메서드로 해결하기 애매한 경우에 사용한다.
- 예시로 POST의 /new, /edit, /delete가 있다(동사).

## 참고하면 좋은 URI 설계 개념
- 문서(document)
  - 단일 개념(파일 하나, 객체 인스턴스, 데이터베이스 row)
  - 예) /members/10, /files/star.jpg
- 컬렉션(collection)
  - 서버가 관리하는 리소스 디렉터리
  - 서버가 리소스의 URI를 생성하고 관리
  - 예) /members
- 스토어(store)
  - 클라이언트가 관리하는 자원 저장소
  - 클라이언트가 리소스의 URI를 알고 관리
  - 예) /files
- 컨트롤러(controller), 컨트롤 URI
  - 문서, 컬렉션, 스토어로 해결하기 어려운 추가 프로세스 실행
  - 동사를 직접 사용
  - 예) /probes/{no}/attack

참고 url: <https://restfulapi.net/resource-naming>
