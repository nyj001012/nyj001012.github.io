---
title: "[Inception] 평가 대비 알아두면 좋은 것들"
excerpt: "Inception을 평가 받을 때 알아두면 좋을 것들"
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
last_modified_at: 2023-09-26T00:00:00+09:00
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