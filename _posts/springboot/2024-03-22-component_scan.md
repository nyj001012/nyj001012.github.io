---
title: "회원 관리 예제 4 - 컴포넌트 스캔과 자동 의존관계 설정"
excerpt: "스프링 컨테이너에 빈 등록하기"
category: 
  - springboot
author_profile: true
sidebar:
  - nav: "main" 
tag:
  - spring boot
  - 회원 관리 예제
  - Bean
  - 의존성
toc: true
toc_sticky: true
last_modified_at: 2024-03-22T00:00:00+09:00
---

> 이 포스트는 김영한님의 ['스프링 입문 - 코드로 배우는 스프링 부트, 웹 MVC, DB 접근 기술'](https://www.inflearn.com/course/%EC%8A%A4%ED%94%84%EB%A7%81-%EC%9E%85%EB%AC%B8-%EC%8A%A4%ED%94%84%EB%A7%81%EB%B6%80%ED%8A%B8/dashboard)을 수강하고 작성하였습니다.  

# 스프링 컨테이너에 빈 등록하기
## 컴포넌트 스캔
- `@Component` 어노테이션이 있으면 스프링 빈으로 자동 등록
- `@Controller` 어노테이션이 붙은 컨트롤러가 자동으로 스프링 빈에 등록된 것도 같은 이유
- `@Component`를 포함하는 다음 어노테이션도 스프링 빈으로 자동 등록
  - `@Controller`
  - `@Service`
  - `@Repository`
- 스프링은 컨테이너에 빈을 등록할 때 싱글톤을 기본으로 함

## 자동 의존관계 설정

```java
@Controller
public class HelloController {

    private final MemberService memberService;

    @Autowired
    public HelloController(MemberService memberService) {
        this.memberService = memberService;
    }

    // ...(생략)
}
```

- `HelloController`는 `MemberService`에 의존하는 관계
  - 예) `HelloController`가 `MemberService`를 통해 회원가입을 시키고 회원 조회를 함
- 스프링 컨테이너에 `MemberService`를 등록하면, 하나의 `MemberService`로 여러 컨트롤러가 사용할 수 있음(싱글톤)
- `@Autowired`로 생성자를 정의하면, 스프링이 `MemberService`와 `HelloContainer`를 연결
  - 생성자가 하나라면 생략 가능
- 스프링이 `MemberService`와 `HelloContainer`를 연결하기 위해서는, `MemberService`가 스프링 빈으로 등록되어 있어야 함
  - `Bean`에 등록되지 않은 컴포넌트에 대해서는 `@Autowired`가 동작하지 않음
    - 예) 내가 직접 `new MemberService()`를 만들고 할당할 경우

```java
@Service
public class MemberService {

    private final MemberRepository memberRepository;

    // @Autowired
    public MemberService(MemberRepository memberRepository) {
        this.memberRepository = memberRepository;
    }

    // ...(생략)
}
```

```java
@Repository
public class MemoryMemberRepository implements MemberRepository {
    private static ConcurrentHashMap<Long, Member> store = new ConcurrentHashMap<>();
    private static AtomicLong sequence = new AtomicLong(0);

    // ...(생략)
}
```

# 언제 사용하나?
- 정형화된 컨트롤러, 서비스, 리포지토리에 사용
