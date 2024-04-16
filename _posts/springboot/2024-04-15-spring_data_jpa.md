---
title: "스프링 Data JPA"
excerpt: ""
category: 
  - springboot
author_profile: true
sidebar:
  - nav: "main" 
tag:
  - spring boot
  - JPA
toc: true
toc_sticky: true
last_modified_at: 2024-04-15T00:00:00+09:00
---

> 이 포스트는 김영한님의 ['스프링 입문 - 코드로 배우는 스프링 부트, 웹 MVC, DB 접근 기술'](https://www.inflearn.com/course/%EC%8A%A4%ED%94%84%EB%A7%81-%EC%9E%85%EB%AC%B8-%EC%8A%A4%ED%94%84%EB%A7%81%EB%B6%80%ED%8A%B8/dashboard)을 수강하고 작성하였습니다.

# `DataJPAMemberRepository` 인터페이스 생성
```java
package hello.hellospring.repository;

import hello.hellospring.domain.Member;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface DataJPAMemberRepository extends JpaRepository<Member, Long>, MemberRepository {
    Optional<Member> findByName(String name);
}
```

# 스프링 설정 파일 `SpringConfig`에서 리포지토리 설정 변경
```java
package hello.hellospring;

// import 생략

@Configuration
public class SpringConfig {

    private final MemberRepository memberRepository;

    public SpringConfig(MemberRepository memberRepository) {
        this.memberRepository = memberRepository;
    }

    @Bean
    public MemberService memberService() {
        return new MemberService(memberRepository);
    }
}
```

리포지토리 설정 부분을 삭제했는데, 스프링 데이터 JPA가 `DataJPAMemberRepository`를 자동으로 스프링 빈에 등록해준다.

# 여담
스프링 데이터 JPA에서 어떤 기능들을 제공하는지 찾아봤는데, `find()`, `findAll()`, `findById()`, `save()`, `count()` 등 내가 ORM을 쓰면서 봤던 함수들이 여럿 보였다. 심지어 하는 일과 원리 또한 ORM이라고 생각했다.  
아니나 다를까, ORM을 지원하는 자바 API가 JPA였다.

JPA와 ORM에 대한 설명은 [여기](https://me-analyzingdata.tistory.com/entry/Spring-JPA-ORM%EA%B3%BC-JPA)에서 잘 정리되어 있어서 링크를 연결해두겠다.
