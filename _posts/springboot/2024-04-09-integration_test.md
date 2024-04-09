---
title: "스프링부트 통합 테스트"
excerpt: "스프링, DB와 함께 테스트하기"
category: 
  - springboot
author_profile: true
sidebar:
  - nav: "main" 
tag:
  - spring boot
  - test
toc: true
toc_sticky: true
last_modified_at: 2024-04-09T00:00:00+09:00
---

> 이 포스트는 김영한님의 ['스프링 입문 - 코드로 배우는 스프링 부트, 웹 MVC, DB 접근 기술'](https://www.inflearn.com/course/%EC%8A%A4%ED%94%84%EB%A7%81-%EC%9E%85%EB%AC%B8-%EC%8A%A4%ED%94%84%EB%A7%81%EB%B6%80%ED%8A%B8/dashboard)을 수강하고 작성하였습니다.

# `MemberServiceIntegrationTest.java` 파일 작성
기존에 `MemberServiceTest.java` 파일을 그대로 복사해서 작성했다. 여기서 단위 테스트때와 몇 가지 차이가 있다.

```java
package hello.hellospring.service;

// import 생략

@SpringBootTest
class MemberServiceIntegrationTest {
    @Autowired MemberService memberService;
    @Autowired MemberRepository memberRepository;

    @Test
    void 회원가입() {
        Member member = new Member();
        member.setName("에진");

        memberService.join(member);

        Optional<Member> findResult = memberRepository.findByName(member.getName());
        Member joinedMember = findResult.get();
        assertThat(member.getName()).isEqualTo(joinedMember.getName());
    }
// ... 이하 내용 생략
```

첫 번째로 `@SpringBootTest`라는 어노테이션이 생겼다. `@SpringBootTest` 어노테이션은 스프링 컨테이너를 테스트할 때 함께 실행하도록 해준다. 그렇게 함으로써 `@Autowired`로 스프링 컨테이너의 객체를 꺼내올 수 있다.

두 번째로 기존에는 `memberService`와 `memberRepository`를 `@BeforeEach`의 `setUp()` 메서드를 통해 생성자로 초기화했다면, 이제는 스프링 컨테이너에 있는 서비스와 리포지토리 객체를 가져올 것이기 때문에 `@Autowired`를 통해 해당 객체들을 가져다 썼다.  
원래 필드에 `@Autowired`를 적용하는 건 추천하지 않는 방법이었으나, 따로 의존성 주입이 이루어질 것도 아니어서 테스트 단계에서는 이렇게 작성하기도 한다더라.

세 번째로 `@BeforeEach`와 `@AfterEach`의 메서드들을 전부 삭제했다. 이 상태로는 테스트를 실행하면 계속해서 DB에 테스트 데이터가 쌓이게 될 것이다.

이 상태로 테스트를 여러 번 실행해보자.

## DB에 테스트 데이터가 저장된다
![test_fail](/assets/images/page/springboot/2024-04-09_test_fail.png)

테스트가 끝나고 결과를 보면 당연히 실패했을 것이다. 실패 사유로 '이미 존재하는 회원입니다.'가 출력되었다.  
실제로 DB를 확인해보면, 아래와 같이 테스트 데이터가 저장되어 있는 것을 볼 수 있다.

![database_duplicate](/assets/images/page/springboot/2024-04-09_database_duplicate.png)

사실 `@AfterEach`로 매 테스트 끝날 때마다 DB를 초기화해주는 함수를 작성하면 그만이지만, 솔직히 조금 귀찮다. 테이블 하나만 있는 거면 몰라도, 여러 테이블이 관계로 엮여있다면?

이걸 도와주기 위해 나온 것이 `@Transactional` 어노테이션이다.

## `@Transactional`: 테스트 트랜잭션 관리

'Transaction'이라는 단어는 어떠한 일의 '완료'를 의미한다. 따라서 한 작업이 끝날 때까지의 단위를 말하며, 이 작업이 끝나야만 DB에 작업 내용이 반영된다.

즉, DB에 내가 작업한 내용을 commit하기 전까지는 실제로 DB에 어떠한 변경 사항도 반영되지 않는다.

`@Transactional` 어노테이션은 아래와 같은 위치에 작성했다.

```java
package hello.hellospring.service;

// import 생략

@SpringBootTest
@Transactional
class MemberServiceIntegrationTest {
  // 이하 생략
}
```

이렇게 하면 매 테스트케이스마다 테스트가 끝나면 rollback이 일어나 실제 DB에는 값이 저장되지 않는다. 따라서 이 상태로 테스트를 여러 번 실행하면 당연히 통과할 것이다.

![test_success](/assets/images/page/springboot/2024-04-09_test_success.png)

# 통합 테스트 관련 어노테이션
> [스프링부트 테스트 관련 공식 문서](https://docs.spring.io/spring-boot/docs/current/reference/html/features.html#features.testing.spring-boot-applications)

## `@SpringBootTest`
스프링 컨테이너에 있는 것(객체라든가)들이 필요할 때 `@ContextConfiguration` 대신 사용한다.

`@SpringBootApplication`으로 지정된 `main()` 메서드를 찾아서 `ApplicationContext`를 생성한다.

## `@Transactional`
기본적으로는 각 테스트 메서드가 끝날 때마다 rollback한다.

그러나 `RANDOM_PORT`나 `DEFINED_PORT`로 `@SpringBootTest`의 옵션을 줘서 실제 servlet 환경을 만들어버리면 HTTP 클라이언트와 서버가 분리된 스레드에서 동작하므로 트랜잭션 또한 분리되어버린다. 그래서 이런 경우에는 서버에서 초기화된 트랜잭션은 rollback되지 않는다.

## `@Commit`
`@Transactional` 어노테이션을 사용하면 기본적으로는 매 테스트 메서드가 끝날 때마다 rollback을 하지만, 이 `@Commit` 어노테이션을 사용하면 해당 테스트 메서드에서 DB를 변경한 내용이 반영된다.
