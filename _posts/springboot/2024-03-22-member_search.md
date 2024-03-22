---
title: "회원 관리 예제 8 - 조회"
excerpt: "웹 MVC 개발"
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

# 템플릿 만들기
```html
<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org">
<head>
    <meta charset="UTF-8" http-equiv="Content-Type">
    <title>Hello Spring</title>
</head>
<body>
<h1>회원 목록</h1>
<table>
    <thead>
    <td>No.</td>
    <td>이름</td>
    </thead>
    <tbody>
    <tr th:each="member : ${members}">
        <td th:text="${member.id}"></td>
        <td th:text="${member.name}"></td>
    </tr>
    </tbody>
</table>
</body>
</html>
```

- thymeleaf를 이용하여 `members`의 필드를 한 줄씩 추가

# `/members` GET 요청 처리하는 컨트롤러 추가
```java
package hello.hellospring.controller;

// import 생략

@Controller
public class MemberController {
    // 생략
    @GetMapping("/members")
    public String getMembers(Model model) {
        List<Member> memberList = memberService.findMembers();
        model.addAttribute("members", memberList);
        return "members/members";
    }
}
```

- `/members` 리소스 GET 요청이 들어오면 실행
- `memberService.findMembers()`로 멤버 목록 받아와서 `model`에 추가
- 템플릿 파일에 `model`을 전달
