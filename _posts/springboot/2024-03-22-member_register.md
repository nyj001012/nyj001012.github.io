---
title: "회원 관리 예제 7 - 회원가입"
excerpt: "웹 MVC 개발"
category: ㄴ
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

# 회원 가입 페이지 GET 요청 처리
```java
package hello.hellospring.controller;

// ...import 생략

@Controller
public class MemberController {
    @GetMapping("/members/sign-up")
    public String getMembersSignUp() {
        return "members/sign-up";
    }
}
```

- `/members/sign-up`이라는 리소스의 GET 요청이 들어오면 `templates/members/sign-up.html`을 가져옴

# 템플릿 만들기
```html
<!-- templates/members/sign-up.html -->

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Hello Spring</title>
</head>
<body>
<h1>회원 가입</h1>
<form action="/members/sign-up" method="post">
    <input type="text" placeholder="이름을 입력하세요" name="name">
    <button type="submit">가입하기</button>
</form>
</body>
</html>
```

- 서버에서는 `<input>`의 `name` 어트리뷰트를 이용하여 `<input>`의 값에 접근
- `<button>`을 클릭하면 `<form>`의 `action` 어트리뷰트에 지정된 곳으로 POST 요청이 갈 것

# 회원 가입 POST 요청 처리
## `<form>` 태그의 데이터 매핑 클래스 생성
```java
package hello.hellospring.controller;

public class MemberForm {
    private String name;

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }
}
```

- 필드명 `name`은 `<input>`의 `name` 어트리뷰트와 동일해야 함

## 회원 가입 POST 요청을 처리하는 컨트롤러 메서드 생성
```java
package hello.hellospring.controller;

// import 생략

@Controller
public class MemberController {
    private final MemberService memberService;

    public MemberController(MemberService memberService) {
        this.memberService = memberService;
    }

    // GetMappging 생략

    @PostMapping("/members/sign-up")
    public String postMembersSignUp(MemberForm form) {
        Member member = new Member();
        member.setName(form.getName());
        memberService.join(member);
        return "redirect:/";
    }
}

```
- `/members/sign-up` 리소스의 POST 요청이 올 경우, 새로운 멤버 객체를 만들어 `MemberService.join()`으로 회원가입
- 가입 후 홈페이지로 리다이렉트
