---
title: "[Inception] 평가를 준비하며, 평가 받으며 알게된 것들"
excerpt: "Inception을 평가를 준비하면서, 그리고 평가 받으며 알게된 것들 정리"
category: 
  - 42_seoul
author_profile: true
sidebar:
  - nav: "main" 
tag:
  - 42서울
  - Inception
toc: true
toc_sticky: true
last_modified_at: 2023-10-03T00:00:00+09:00
---

# ssh 설정
> [Born2beroot를 마치고 - SSH](https://nyj001012.github.io/42_seoul/born2beroot/#ssh)
여깄는 거 그대로 하면 된다.

# 호스트 파일(로컬)을 원격 환경(VM)으로 옮기기
> 참고: [리눅스 scp 명령어 사용법 ( 파일 전송 프로토콜 / 파일 보내기 /파일 받기 )](https://wlsvud84.tistory.com/11)
```bash
scp -P PORT -r FILE_NAME REMOTE_ID@REMOTE_IP:PATH_TO
scp -P 4242 -r inception yena@127.0.0.1:/tmp  # 예시
```

# PID 1
> Read about PID 1 and the best practices for writing Dockerfiles.

서브젝트에 보면 이런 문구가 있다. 그래서 Dockerfile을 잘 작성하기 위해 PID 1이 뭔지 알아봤다.

> 참고: [How better management of processes in Docker can greatly improve a container’s lifecycle](https://www.padok.fr/en/blog/docker-processes-container)

## PID 1의 역할
1. Init 프로세스 역할
2. 종료 시그널 처리
3. 종료 후 클린업
4. 컨테이너 관리

각 프로세스는 PID와 PPID(부모의 PID)를 가지고 있다(pipex와 minishell을 했다면 알 것이다).  
유닉스 프로세스는 트리로 정렬된다. 각 프로세스는 자식 프로세스를 가질 수 있고, 제일 상위(첫 번째) 프로세스인 PID 1을 제외하고 모두 부모 프로세스가 있다.

PID 1은 초기화로 알려져 있는데, 모든 프로세스의 조상이며 모든 프로세스가 동작하는 데 토대의 역할을 한다.

만약 프로세스가 종료되면, 일부 데이터는 부모 프로세스가 가져갈 때까지 그대로 남아있다. 만약 부모 프로세스가 그 데이터를 가져가지 않는다면, 좀비 프로세스가 된다.  
만약 부모 프로세스가 종료되면, 그 자식 프로세스는 고아가 되고 또다른 프로세스의 자식이 되기도 한다. 때로는 초기화 프로세스의 자식 프로세스가 된다.

`mycontainer`라는 이름의 도커 컨테이너가 실행중이라고 해보자. 내가 그 컨테이너를 멈추고 싶을 때 `docker stop mycontainer`를 실행한다.

PID 1은 SIGTERM 시그널을 받는다. PID 1은 이 시그널을 자식 프로세스에 전달한다. 모든 자식 프로세스는 동작을 멈추고 실행이 종료됨을 의미하는 SIGCHILD 시그널과 exit status를 부모 프로세스로 보낸다. PID 1은 모든 자식이 종료될 때까지 기다린다.  
더이상 PID 1에 자식이 없다면, exit status를 0으로 하여 실행을 종료한다.

## CMD, ENTRYPOINT
CMD, ENTRYPOINT는 컨테이너가 시작될 때 실행되는 명령 또는 실행 파일을 정의하는 데 사용된다. 따라서 PID 1로 설정되는 프로세스는 일반적으로 CMD 또는 ENTRYPOINT로 지정된 명령이 된다.

PID 1을 올바르게 설정하고 시그널을 처리하는 것은(= CMD와 ENTRYPOINT로 명령을 적절하게 실행하는 것은) 도커 컨테이너의 안정성과 정상적인 작동을 보장하는 데 중요하다.

그래서 좋은 도커 파일을 작성하기 위해 PID 1에 대해 알아보라는 것이었다.

### CMD
```Dockerfile
CMD ["app", "--option"]
```
- 이미지를 빌드할 때 컨테이너에서 실행될 명령어를 정의한다.
- Dockerfile에서 한 번만 사용할 수 있다.
- `docker run` 명령어를 사용하여 오버라이드 가능하다.

### ENTRYPOINT
```Dockerfile
ENTRYPOINT ["app"]
```
- 컨테이너가 실행될 때 수행할 명령을 정의한다.
- Dockerfile에서 한 번만 사용할 수 있다.
- `docker run --entrypoint` 명령어를 사용하여 오버라이드 가능하다.

# /etc/hosts
> 참고: [/etc/hosts 파일은 무엇인가](https://mytory.net/archives/13134)

/etc/hosts 파일은 도메인의 IP를 찾을 때 컴퓨터가 맨 처음 조사하는 파일이다. 여기서 IP 주소를 찾으면, 컴퓨터는 이 도메인에 대해 DNS 서버에는 묻지 않는다. 즉, DNS 서버를 거치지 않고서도 도메인으로 사이트에 접근 가능한 것이다.

내가 Inception 과제를 진행할 때 의문이었던 점이 있었다. login.42.fr이라는 도메인으로 사이트에 접속하려면 DNS에 접근해야 할텐데, 그러려면 DNS에 내가 저 도메인을 등록해놔야 하는 거 아닌가? 그러면 도메인을 사야할텐데? 싶었다.  
그런데 그냥 /etc/hosts에 있는 내용을 바꿔주기만 하면 DNS에 접근하지 않더라도 도메인 이름을 사용할 수 있었다.

# docker-compose.yml
## version
### 만약 version이 3이라면 어떻게 될까?
만약 docker compose version을 3이라고 명시하면 도커는 어떤 버전으로 인식할까?

```yml
version: '3'
```

`version: 3`일 경우, `3.x` 버전을 의미하므로 메이저 버전이 3인 것 중 가장 최신 버전이 적용된다.

## volumes
### driver_opts
특정 볼륨 드라이버에 대한 구성 옵션을 설정하는 데 사용한다.

- `type`: 어떤 유형의 드라이버를 사용할 것인지 지정한다.
  - ex) local(default), nfs, bind, volume, aws, etc.
  - `none`의 경우, 볼륨을 생성하지 않고 컨테이너와 호스트 간 파일을 공유한다.
- `o`: 추가적인 마운트 옵션을 설정하는 데 사용한다.
  - `bind`: 호스트 파일 시스템의 특정 경로를 컨테이너 내부 경로와 바인드한다.

```yml
volumes:
  ...
  - type: none
    o: bind
```
일 경우, 볼륨을 생성하지 않고 컨테이너와 호스트 간 파일을 공유하기 때문에 호스트 파일 시스템의 특정 경로를 컨테이너 내부 경로와 바인드한다. 즉, 호스트 측의 볼륨과 컨테이너 내부 볼륨이 동기화되어 호스트에서 볼륨에 파일을 추가하면 컨테이너 내부 볼륨에도 파일이 추가된다.

# nginx
## nginx란?
> 참고: [What Is NGINX?](https://www.nginx.com/resources/glossary/nginx/)

> 한 마디로 정리하자면 빠르고 효율적으로 자원을 사용하는 웹 서버

**NGINX**는 웹 서빙, 리버스 프록싱, 캐싱, 로드 밸런싱, 미디어 스트리밍 등을 위한 오픈 소스 소프트웨어이다.  
HTTP 서버 기능 뿐만 아니라 NGINX는 이메일을 위한 프록시 서버와 리버스 프록시, 그리고 HTTP, TCP, UDP 서버의 로드 밸런서 기능도 수행할 수 있다.

### 웹 서버로써의 NGINX
NGINX의 목표는 가장 **빠른** 웹 서버를 만들고 그 우수함을 유지하는 것이다. NGINX는 아파치(Apache)와 기타 다른 서버들보다 웹 서버 성능 측정 벤치마크에서 꾸준히 좋은 성적을 보여주고 있다.  

### 웹 서빙을 넘어선 NGINX
NGINX는 흔히 리버스 프록시와 로드 밸런서로 사용되며 들어오는 트래픽을 관리하고 그 트래픽을 더 느린 상위 서버로 분배한다.  

NGINX는 클라이언트와 두 번째 웹 서버 사이에 자주 배치되어 SSL/TLS 단말기 또는 웹 가속기의 역할을 한다(그래서 이번 Inception 과제에서는 SSL 세팅을 NGINX에서 한다).  
Node.js부터 PHP까지 어느 언어로 빌드된 동적 웹사이트라도 일반적으로 NGINX를 콘텐트 캐시와 리버스 프록시로써 배포한다. 이는 어플리케이션 서버로의 로드(load)를 줄이고 하드웨어를 가장 효율적으로 사용하게끔 한다.

# php-fpm
## PHP
> 참고: <https://www.php.net/manual/en/intro-whatis.php>

PHP는 널리 사용되는 오픈 소스 범용 스크립팅 언어이며, 특히 웹 개발에 적합하고 HTML에 같이 사용할 수 있다.

## CGI
> 참고: [공용 게이트웨이 인터페이스](https://ko.wikipedia.org/wiki/%EA%B3%B5%EC%9A%A9_%EA%B2%8C%EC%9D%B4%ED%8A%B8%EC%9B%A8%EC%9D%B4_%EC%9D%B8%ED%84%B0%ED%8E%98%EC%9D%B4%EC%8A%A4)

CGI(Common Gateway Interface)는 웹 서버 상에서 사용자 프로그램을 동작시키기 위한 조합으로, 서버 프로그램과 외부 프로그램과의 연계법을 정한 것이다.

CGI는 인터페이스로, 특정 플랫폼에 의존하지 않기 때문에 프로그램 본체를 CGI로 부르는 것은 잘못된 것이다.

쉽게 말해서 서버에서 사용자 요청을 받아 데이터를 동적으로 생성하고 클라이언트에 보내주기 위해 외부 프로그램에서 서버와 어떻게 협업할 것인지를 정해놓은 것 같다.

## FPM(FastCGI Process Manager)
> 참고: [FastCGI Process Manager (FPM)](https://www.php.net/manual/en/install.fpm.php)
FPM은 무거운 사이트에 유용한 것들을 담고 있는 주요 PHP FastCGI 구현체이다.  
FPM에는 다음과 같은 것들이 포함되어 있다.

- 안정적인(graceful) 멈춤/시작으로 높은 수준의 프로세스 관리
- 다른 uid/gid/chroot/environment를 가지며, 다른 php.ini를 사용하고 다른 포트를 수신하는 작업자(worker)를 시작할 수 있는 풀 (안전 모드를 대체한다)
- 설정 가능한 stdout과 stderr 로깅
- 갑작스러운 opcode 캐시 파괴로 인한 긴급 재시작
- 업로드 지원 가속
- slowlog
- fastcgi_finish_request
- 동적/요청에 따른/정적 자식 생성
- 다양한 형식을 지원하는 기본적이고 확장된 스테이터스 정보
- php.ini

# wordpress
## wordpress란?
> 참고: [워드프레스](https://ko.wikipedia.org/wiki/%EC%9B%8C%EB%93%9C%ED%94%84%EB%A0%88%EC%8A%A4)

워드프레스는 세계 최대의 자유 오픈 소프트웨어 저작물 관리 시스템이다.  
PHP로 작성되었고, MySQL이나 MariaDB가 주로 사용된다.

# mariaDB
## 왜 MySQL과 MariaDB는 명령어가 똑같고, 사람들이 혼용하는걸까?
> 참고: [MariaDB](https://ko.wikipedia.org/wiki/MariaDB)

MariaDB가 MySQL을 기반으로 만들어졌고, MySQL API와 명령에 정확히 매칭하여 교체 가능성을 높이려 했기 때문에 둘은 높은 호환성을 가지고 있다. 그래서 사용방법에 구조에 엔진까지 거의 동일하게 사용하고 있다. 

# 알파인 리눅스
> 참고: <https://alpinelinux.org/about/>

## 알파인 리눅스의 경량화 방식
> Alpine Linux is built around musl libc and busybox. This makes it small and very resource efficient.

알파인 리눅스는 musl libc와 busybox로 빌드되었다고 한다. 덕분에 용량이 작고 자원을 효율적으로 사용할 수 있다고 한다.

그 둘의 역할로 알파인 리눅스는 많이 사용하는 명령어 또는 옵션만 추려내어 사용하는 방식으로 경량화를 했다고 한다.

### musl libc
> 참고: <https://musl.libc.org/>

musl libc는 Linux system call API 상위에 구현된 C 표준라이브러리로, POSIX를 기반으로 한다.

### busybox
> 참고: <https://busybox.net/about.html>

BusyBox는 많은 공통 UNIX 유틸리티의 버전들을 하나의 작은 실행가능한 파일로 합친 것이다. BusyBox에 있는 유틸리티들은 일반적으로는 모든 기능을 갖춘 GNU 계통보다 적은 옵션을 갖고 있지만, 그 옵션들은 사용자가 기대한(expected) 기능을 제공하고 GNU와 비슷하게 동작한다.  
BusyBox는 작은 시스템 또는 임베디드 시스템에 상당히 완전한 환경을 제공한다.