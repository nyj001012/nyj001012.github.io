---
title: "회원 관리 예제 3 - 서비스"
excerpt: "회원 관리 서비스 개발 및 테스트 예제"
category: 
  - springboot
author_profile: true
sidebar:
  - nav: "main" 
tag:
  - spring boot
  - 회원 관리 예제
toc: true
toc_sticky: true
last_modified_at: 2024-03-22T00:00:00+09:00
---

> 이 포스트는 김영한님의 ['스프링 입문 - 코드로 배우는 스프링 부트, 웹 MVC, DB 접근 기술'](https://www.inflearn.com/course/%EC%8A%A4%ED%94%84%EB%A7%81-%EC%9E%85%EB%AC%B8-%EC%8A%A4%ED%94%84%EB%A7%81%EB%B6%80%ED%8A%B8/dashboard)을 수강하고 작성하였습니다.  

# 회원 서비스 작성
```java
package hello.hellospring.service;

import hello.hellospring.domain.Member;
import hello.hellospring.repository.MemberRepository;
import hello.hellospring.repository.MemoryMemberRepository;

import java.util.List;
import java.util.Optional;

public class MemberService {
    public MemberService(MemberRepository memberRepository) {
        this.memberRepository = memberRepository;
    }

    private final MemberRepository memberRepository;

    /**
     * 회원 가입
     *
     * @param member 가입할 멤버 객체
     * @return 가입한 멤버 객체의 id
     */
    public Long join(Member member) {
        validateDuplicateMember(member);

        memberRepository.save(member);
        return member.getId();
    }

    /**
     * 중복 회원 검사
     * @param member 검사할 회원
     */
    private void validateDuplicateMember(Member member) {
        memberRepository.findByName(member.getName())
                .ifPresent(m -> {
                    throw new IllegalStateException("이미 존재하는 회원입니다.");
                });
    }

    /**
     * 전체 회원 조회
     * @return 전체 회원 리스트
     */
    public List<Member> findMembers() {
        return memberRepository.findAll();
    }

    /**
     * id로 한 회원 조회
     * @param memberId 조회할 회원의 Id
     * @return Member의 Optional 객체
     */
    public Optional<Member> findOneById(Long memberId) {
        return memberRepository.findById(memberId);
    }
}

```

## 테스트 작성
```java
package hello.hellospring.service;

import hello.hellospring.domain.Member;
import hello.hellospring.repository.MemoryMemberRepository;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.Optional;

import static org.assertj.core.api.Assertions.assertThat;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.fail;


class MemberServiceTest {
    MemberService memberService;
    MemoryMemberRepository memoryMemberRepository;

    @BeforeEach
    void setUp() {
        memoryMemberRepository = new MemoryMemberRepository();
        memberService = new MemberService(memoryMemberRepository);
    }

    @AfterEach
    void tearDown() {
        memoryMemberRepository.clearStore();
    }

    @Test
    void 회원가입() {
        Member member = new Member();
        member.setName("에진");

        memberService.join(member);

        Optional<Member> findResult = memoryMemberRepository.findByName(member.getName());
        Member joinedMember = findResult.get();
        assertThat(member.getName()).isEqualTo(joinedMember.getName());
    }

    @Test
    void 회원가입_중복_유저() {
        Member member1 = new Member();
        Member member2 = new Member();
        member1.setName("예진");
        member2.setName("예진");

        memberService.join(member1);

        IllegalStateException e = assertThrows(IllegalStateException.class, () -> memberService.join(member2));
        assertThat(e.getMessage()).isEqualTo("이미 존재하는 회원입니다.");
    }

    @Test
    void 모든_멤버_리스트_가져오기() {
        for (int i = 0; i < 10; i++) {
            Member member = new Member();
            member.setName(Integer.toString(i) + "번째 유저");
            memberService.join(member);
        }

        List<Member> members = memberService.findMembers();

        assertThat(members.size()).isEqualTo(10);
    }

    @Test
    void id로_멤버_찾기() {
        Member member1 = new Member();
        Member member2 = new Member();
        member1.setName("피카츄");
        member2.setName("리자몽");
        memberService.join(member1);
        memberService.join(member2);

        Optional<Member> findResult = memberService.findOneById(member1.getId());

        findResult.ifPresentOrElse(member -> {
            assertThat(member.getName()).isEqualTo(member1.getName());
        }, () -> {
            fail();
        });
    }

    @Test
    void 없는_id로_멤버_찾기() {
        Member member1 = new Member();
        member1.setName("피카츄");
        memberService.join(member1);

        Optional<Member> findResult = memberService.findOneById(-1L);

        assertThat(findResult.isEmpty()).isTrue();
    }
}

```

테스트 함수 한글로 적어도 된다니 신세계다..! 이번 서비스 함수의 테스트 코드를 작성해보면서 예외 처리 테스트는 어떻게 작성할 수 있는지를 알 수 있었다.

또한 Service 객체에서 Repository 객체를 가지고 있는데, 이를 테스트 단계에서 따로 만들어서 사용하면 별개의 Repository 객체가 생겨버린다. 때문에 의존성 주입을 통해 Service 객체의 생성자의 매개변수로 Repository 객체를 넘겨줌으로써 해결할 수 있었다.

테스트 꿀잼
