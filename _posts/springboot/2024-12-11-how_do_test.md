---
title: "스프링부트에서 테스트하기"
excerpt: "이리밸 프로젝트를 하며 진행했던 테스트 방법들에 대한 정리"
category: 
  - web
  - react
author_profile: true
sidebar:
  - nav: "main" 
tag:
  - web
  - test
  - springboot
  - 이터널 리턴
  - 밸런스 게임
toc: true
toc_sticky: true
last_modified_at: 2024-12-17T00:00:00+09:00
---

# 테스트를 어떻게 할까?
## 사용한 라이브러리와 모듈
### JUnit5
JUnit5는 테스트 프레임워크로, 단위 테스트에 사용하였다.

### WebMVC
스프링 프레임워크에서 제공하는 모듈로, MVC 패턴을 기반으로 한다.  
나는 테스트 시, `@WebMvcTest`로 컨트롤러를 테스트하는 데 사용했다.

### Mockito
Mockito는 단위 테스트 작성 시 Mock 객체를 생성하고 관리한다.  
의존성을 가짜 객체로 대체하여 테스트를 실행할 수 있기 때문에, 컨트롤러 테스트를 작성할 때 서비스 의존성을 가짜 서비스 객체로 대체하여 사용했다.

## 리포지토리
### 중점으로 본 것
리포지토리를 테스트 할 때 JPA를 통해 데이터베이스와 통신하며, 각 함수의 동작이 의도한 대로 데이터베이스에 영향을 주었는지를 확인했다.

## 서비스
### 중점으로 본 것
서비스 함수는 비즈니스 로직에 따라 인자를 적절히 가공하고, 리포지토리 함수를 올바르게 호출하는지 확인했다.  
따라서 단위 테스트 작성 시, 비즈니스 로직에 명시된 모든 경우의 수와 리포지토리 함수 호출 여부를 검증했다.

## 컨트롤러
### 중점으로 본 것
컨트롤러 함수는 여러 Request 객체를 처리할 때, 서비스 객체가 각 Request에 맞는 값을 반환하면 그 값을 바탕으로 의도된 응답을 반환하는지 확인했다.

# 테스트 커버리지
## 커버리지란
테스트 커버리지는 코드에서 얼마나 많은 부분이 테스트되었는지를 나타내는 지표다.

- 코드 라인 커버리지: 전체 코드 라인 중 테스트를 통해 실행된 코드 라인의 비율
- 분기 커버리지: 조건문(if, switch 등)의 모든 분기(예: true/false)를 테스트했는지 측정
- 조건 커버리지: 조건식의 각 개별 조건이 모두 테스트되었는지 측정
  - 예) `if (A && B)`가 있을 때, `A`와 `B` 각각이 `true`와 `false`를 테스트
- 함수 커버리지: 코드의 함수나 메서드가 테스트에서 호출되었는지 측정

## IDE 세팅(IntelliJ)
> 2024.2 버전 기준으로 작성

설정(맥: `⌘ + ,`)에서 `빌드, 실행, 배포` 탭의 `커버리지`에서 `테스트 커버리지당 추적` 체크

## 커버리지 결과 예시
![테스트 커버리지1](/assets/images/page/springboot/2024-12-17_test_coverage_example1.png)
커버리지 결과는 테스트한 클래스와 메서드 개수, 줄 수, 브랜치 수를 전부 보여준다.

![테스트 커버리지2](/assets/images/page/springboot/2024-12-17_test_coverage_example2.png)
커버리지가 활성화되어 있을 때 코드에 포커싱하면 위와 같이 테스트 커버리지가 나온다.  
`choiceA.isBlank()`와 `choiceB.isBlank()`의 `true 도달: 0`인 것을 보아 해당 조건들이 false일 때에만 테스트를 수행했다는 의미이므로, 조건 커버리지가 부족함을 알 수 있다.
