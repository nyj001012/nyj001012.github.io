---
title: "프로젝트 환경설정"
excerpt: ""
category: 
  - springboot
author_profile: true
sidebar:
  - nav: "main" 
tag:
  - spring boot
toc: true
toc_sticky: true
last_modified_at: 2022-03-16T00:00:00+09:00
---
> 이 포스트는 김영한님의 ['스프링 입문 - 코드로 배우는 스프링 부트, 웹 MVC, DB 접근 기술'](https://www.inflearn.com/course/%EC%8A%A4%ED%94%84%EB%A7%81-%EC%9E%85%EB%AC%B8-%EC%8A%A4%ED%94%84%EB%A7%81%EB%B6%80%ED%8A%B8/dashboard)을 수강하고 작성하였습니다.  

# 프로젝트 생성
[[Mac] 스프링 부트 시작](/springboot/mac_intellij)

# 라이브러리 살펴보기
gradle이나 maven과 같은 빌드 툴들은 의존 관계를 관리한다.  
만약 내가 A라는 라이브러리만 필요하지만, A는 B라는 라이브러리에 의존하기 때문에 빌드 툴은 A와 B를 함께 빌드한다.

## 스프링 부트 라이브러리
- spring-boot-starter-web
  - spring-boot-starter-tomcat: 톰캣 (웹 서버)
  - spring-webmvc: 스프링 웹 MVC
  - spring-boot-starter-thymeleaf: 타임리프 템플릿 엔진(View)
  - spring-boot-starter(공통): 스프링 부트 + 스프링 코어 + 로깅
    - spring-boot
      - spring-core
    - spring-boot-starter-logging
      - logback, slf4j

## 테스트 라이브러리
- spring-boot-starter-test
  - junit: 테스트 프레임워크
  - mockito: 목 라이브러리
  - assertj: 테스트 코드를 좀 더 편하게 작성하게 도와주는 라이브러리
  - spring-test: 스프링 통합 테스트 지원