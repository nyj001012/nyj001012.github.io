---
title: "회원 관리 예제 6 - 홈 화면 추가"
excerpt: "웹 MVC 개발"
category: 
  - springboot
author_profile: true
sidebar:
  - nav: "main" 
tag:
  - spring boot
  - thymeleaf
  - 회원 관리 예제
toc: true
toc_sticky: true
last_modified_at: 2024-03-22T00:00:00+09:00
---

> 이 포스트는 김영한님의 ['스프링 입문 - 코드로 배우는 스프링 부트, 웹 MVC, DB 접근 기술'](https://www.inflearn.com/course/%EC%8A%A4%ED%94%84%EB%A7%81-%EC%9E%85%EB%AC%B8-%EC%8A%A4%ED%94%84%EB%A7%81%EB%B6%80%ED%8A%B8/dashboard)을 수강하고 작성하였습니다.  

# 컨트롤러 추가
```java
package hello.hellospring.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class HomeController {
    @GetMapping("/")
    public String home() {
        return "home";
    }
}
```

- 홈(`/`)으로의 GET 요청을 처리하는 컨트롤러 추가
- 요청이 오면 `home.html`을 렌더하도록 설정

# 템플릿 추가
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Hello Spring</title>
</head>
<body>
<h1>Hello Spring!</h1>
<a href="/members/sign-up">회원 가입</a>
<a href="/members">회원 목록</a>
</body>
</html>
```
