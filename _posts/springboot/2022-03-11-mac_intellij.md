---
title: "[Mac] 스프링 부트 시작"
excerpt: ""
category: 
  - springboot
author_profile: true
sidebar:
  - nav: "main" 
tag:
  - IntelliJ
  - spring boot
toc: true
toc_sticky: true
last_modified_at: 2022-03-11T00:00:00+09:00
---
> 이 포스트는 김영한님의 ['스프링 입문 - 코드로 배우는 스프링 부트, 웹 MVC, DB 접근 기술'](https://www.inflearn.com/course/%EC%8A%A4%ED%94%84%EB%A7%81-%EC%9E%85%EB%AC%B8-%EC%8A%A4%ED%94%84%EB%A7%81%EB%B6%80%ED%8A%B8/dashboard)을 수강하고 작성하였습니다.  

# 자바 11 설치
다운로드 링크: <https://www.oracle.com/java/technologies/downloads/#java11-mac>

![java11](/assets/images/page/springboot/2022-03-11_java11.png)

위의 링크에 접속해서 Java SE 11 버전의 .dmg 파일을 다운받아서 실행했다.

설치 과정은 특별할 건 없었고, 하나 신기했던 점은 윈도우와 다르게 환경 변수 설정을 안 해줘도 된다는 것이었다.

# IntelliJ Ultimate 설치
## 학생 라이센스 발급
원래 IntelliJ Ultimate은 유료라서 정액제로 일정 금액을 내야 한다. 그런데 나는 혹시나 학생 계정으로 다운받으면 조금 싸게 해주지 않을까 해서 학생 라이센스를 발급받아 설치했다. 그리고 설치가 끝난 뒤 깨달은 놀라운 점은 학생 라이센스로 IntelliJ Ultimate를 무료로 사용할 수 있다는 것이었다.  
학생 라이센스 발급 과정은 아래와 같다.

[여기](https://www.jetbrains.com/ko-kr/idea/buy/#discounts)에 접속하여 학생 및 교사용의 **자세히 알아보기** 클릭

![license1](/assets/images/page/springboot/2022-03-11_license1.png)

그러면 아래와 같은 페이지가 나올건데, 쭉 스크롤을 내리다가 **지금 신청하기**를 클릭한다.

![license2](/assets/images/page/springboot/2022-03-11_license2.png)

이후 공란을 전부 채워준다. 보통 "14세 이상입니다."를 체크하게 하는 경우를 많이 봤는데, 특이하게도 13세 미만인지를 묻고 있었다.

![license3](/assets/images/page/springboot/2022-03-11_license3.png)

**무료 제품 신청**을 클릭하면 아마 입력했던 이메일 주소로 메일이 왔을 것이다. 나 같은 경우에는 이미 JetBrains Educational Pack에 내 이메일 주소가 사용된 적이 있다는 뜻이었다(엥?). 그래서 클릭하라는 "Please click this link to proceed:" 밑에 있는 링크를 클릭했다.

![license4](/assets/images/page/springboot/2022-03-11_license4.png)

그 링크에 접속하니까 아래와 같은 페이지가 나오면서 계속 하라고 한다. 그래서 **Get started to use** 버튼을 클릭했다.

![license5](/assets/images/page/springboot/2022-03-11_license5.png)

이후에 JetBrains 로그인 페이지가 나온다. 나의 경우, 이메일이 이미 가입되어 있는 상태라 그냥 로그인 했다. 아마 처음 가입을 한 사람들의 경우에는 새로 회원가입을 해야 할 것이다.  
로그인을 하면 아래와 같은 페이지가 나온다. 여기서 **IntelliJ IDEA Ultimate**을 클릭해서 다운로드 페이지로 이동한다.

![license6](/assets/images/page/springboot/2022-03-11_license6.png)

다운로드 페이지에서 **.dmg(Apple Silicon)**을 다운받는다.

![license7](/assets/images/page/springboot/2022-03-11_license7.png)

설치가 끝나고 IntelliJ를 실행하면 로그인 하라는 창이 뜬다. 아까 학생 라이센스를 발급 받았던 계정으로 로그인 하면 아래와 같은 창이 뜨고, 인증이 성공적으로 진행된다.

![license8](/assets/images/page/springboot/2022-03-11_license8.png)

## IntelliJ 설정
IntelliJ 설치가 끝났으니 약간의 설정을 할 것이다. 이후 추가적으로 설정한 것이 있다면 지속적으로 업데이트 할 것이다.

### Gradle 빌드 설정
`⌘ + ,`를 눌러서 환경 설정(Preferences) 창을 열자. 거기서 `빌드, 실행, 배포 > 빌드 도구 > Gradle`에서 **빌드 및 실행을 전부 IntelliJ IDEA**로 바꿔준다. 그래야 gradle을 통해 실행을 하지 않고, 바로 IntelliJ에서 실행함으로써 속도가 빨라진다.

![gradle_config](/assets/images/page/springboot/2022-03-11_gradle_config.png)

# 스프링 부트 프로젝트
## 프로젝트 생성
원래라면 Spring initializr 페이지에 가서 여러 세팅을 해야 하지만, 파일 다운받고 압축 풀고 하는 게 매우매우매우 귀찮다([Spring initializr 참고](/springboot/66-IntelliJ-Spring-Boot-Setting/)). 그런데 IntelliJ Ultimate은 IntelliJ 내에서 저 설정 과정의 모든 걸 해결할 수 있다.

![new_project1](/assets/images/page/springboot/2022-03-11_new_project1.png)

- Language: **Java** / Kotlin / Groovy
- Type: Maven / **Gradle**
- Group: 보통 기업명을 쓴다고 한다
- Artifact: 빌드의 결과물, 즉 프로젝트명(Name)

![new_project2](/assets/images/page/springboot/2022-03-11_new_project2.png)

- Spring Boot: SNAP SHOT이라든가, M1같은 것도 있을 수 있다. 그 친구들은 정식 버전이 아니므로, Release 중에 하나인 **2.6.4**을 골랐다.
- Dependencies: 프로젝트에 추가할 라이브러리
  - Web > **Spring Web**
  - Template Engines > **Thymeleaf**

▼ 프로젝트 생성 완료
![new_project3](/assets/images/page/springboot/2022-03-11_new_project3.png)

## 프로젝트 구조
### .idea
![.idea](/assets/images/page/springboot/2022-03-11_.idea.png)

IntelliJ가 사용하는 설정 파일 포함

### gradle
![gradle](/assets/images/page/springboot/2022-03-11_gradle.png)

gradle 환경을 정리한 파일(wrapper) 포함

### src
![src](/assets/images/page/springboot/2022-03-11_src.png)  

#### src/main
- java - 패키지와 실제 소스 파일들 포함
- resources - 실제 자바 코드를 제외한 xml, properties, html 등의 파일 포함

#### src/test
테스트 코드들과 관련된 소스 포함

### .gitignore
![.gitignore](/assets/images/page/springboot/2022-03-11_gitignore.png)

깃 추적에서 제외시킬 파일/폴더 목록

### build.gradle
![build.gradle](/assets/images/page/springboot/2022-03-11_build.gradle.png)

프로젝트 생성할 때 선택했던 자바의 버전, 라이브러리들에 대한 설정

- `mavenCentral()` - `dependencies` 목록을 maven central 사이트에서 다운받게 설정

## 프로젝트 실행
메인 함수를 실행한다.
![run](/assets/images/page/springboot/2022-03-11_run1.png)

`Tomcat started on port(s): 8080`로 현재 **localhost:8080**에 프로젝트가 올라가있음을 알 수 있다. 스프링 부트는 Tomcat이라는 웹 서버를 내장하고 있기 때문에, Tomcat을 자체적으로 띄울 수 있다.
![terminal](/assets/images/page/springboot/2022-03-11_run2.png)

추가적으로 해당 페이지에 접속하면 아래와 같은 페이지가 뜬다.
![web](/assets/images/page/springboot/2022-03-11_run3.png)
