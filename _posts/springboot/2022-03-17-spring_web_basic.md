---
title: "스프링 웹 개발 기초"
excerpt: ""
category: 
  - springboot
author_profile: true
sidebar:
  - nav: "main" 
tag:
  - spring boot
  - thymeleaf
toc: true
toc_sticky: true
last_modified_at: 2022-03-17T00:00:00+09:00
---
> 이 포스트는 김영한님의 ['스프링 입문 - 코드로 배우는 스프링 부트, 웹 MVC, DB 접근 기술'](https://www.inflearn.com/course/%EC%8A%A4%ED%94%84%EB%A7%81-%EC%9E%85%EB%AC%B8-%EC%8A%A4%ED%94%84%EB%A7%81%EB%B6%80%ED%8A%B8/dashboard)을 수강하고 작성하였습니다.  

# 정적 컨텐츠
정적 컨텐츠는 서버에서의 별도 동작 없이 파일을 그대로 브라우저에 내려주는 것을 말한다.

# MVC와 템플릿 엔진
MVC = Model + View + Controller  
템플릿 엔진은 HTML 파일을 그냥 브라우저에 전달하는 것이 아니라, 서버에서 별도의 동작을 한 후에 데이터를 동적으로 변환하여 전달한다.

# API
API는 json과 같은 포맷으로 클라이언트에 전달하는 방식이다. 주로 서버 - 서버가 데이터를 주고 받을 때 사용한다.