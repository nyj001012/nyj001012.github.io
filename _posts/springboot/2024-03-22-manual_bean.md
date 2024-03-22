---
title: "회원 관리 예제 5 - 자바 코드로 직접 스프링 빈 등록하기"
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
## 자바 코드로 직접 등록

`@Controller`를 제외한 다른 컴포넌트 어노테이션 제거 후 진행

```java
// [package]/SpringConfig.java
package hello.hellospring;

import hello.hellospring.repository.MemberRepository;
import hello.hellospring.repository.MemoryMemberRepository;
import hello.hellospring.service.MemberService;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class SpringConfig {

    @Bean
    public MemberService memberService() {
        return new MemberService(memberRepository());
    }

    @Bean
    public MemberRepository memberRepository() {
        return new MemoryMemberRepository();
    }
}
```

- `@Configuration` 어노테이션 이용하여 설정 파일임을 스프링에 명시
- XML로도 설정할 수 있지만, 최근에는 잘 사용하지 않음
- `MemoryMemberRepository`를 `DBRepository`로 바꿀 것이기 때문에 해당 방식 사용

## 의존성 주입 (DI; Dependency Injection)
### 생성자 주입(권장)
```java
@Controller
public class HelloController {

    private final MemberService memberService;

    @Autowired
    public HelloController(MemberService memberService) {
        this.memberService = memberService;
    }
}
```

- 생성자의 매개변수로 의존성을 주입하는 방식
- 처음 스프링 컨테이너가 로드될 때 한 번 실행되기 때문에, 변경될 여지가 없음

### 필드 주입
```java
public class HelloController {

    @Autowired private final MemberService memberService;
}
```

- 필드에 `@Autowired` 어노테이션을 작성하는 방식
- `memberService`를 중간에 대체할 수 있는 방법이 없음

### Setter 주입
```java
public class HelloController {

    private MemberService memberService;

    @Autowired
    public void setMemberService(MemberService memberService) {
        this.memberService = memberService;
    }
}
```

- 필드의 setter에 `@Autowired`로 의존성 주입을 하는 방식
- `public` 메서드이기 때문에, 모두에게 노출
  - 의도치 않은 변수로 바뀔 가능성 있음
  - `MemberService`의 경우 로드 시점에만 한 번만 할당하면 되기 때문에 위의 방식에 맞지 않음
