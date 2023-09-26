---
title: "[Inception] 알파인 리눅스를 사용하며 배운 것"
excerpt: ""
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
last_modified_at: 2023-08-20T00:00:00+09:00
---

# sudo, usermod 없음
> 참고: [How do I add a user when I'm using Alpine as a base image?
](https://stackoverflow.com/questions/49955097/how-do-i-add-a-user-when-im-using-alpine-as-a-base-image)

알파인 리눅스에는 sudo, usermod 명령어가 없기 때문에, 일반 사용자가 도커를 관리하려면

```shell
# adduser [OPTION] USER GROUP
adduser [USERNAME] docker
```

또는

```shell
addgroup [USERNAME] docker
```

의 명령어로 일반 유저를 사용자 그룹에 추가해야 한다.

사용자가 특정 그룹에 속해있는지 확인하는 명령어는 다음과 같다.
```shell
groups [USERNAME]
```

# 그룹 관리를 더 편하게 할 수 있도록 도와주는 gpasswd

> 참고: [리눅스-gpasswd 명령어](https://m.blog.naver.com/PostView.nhn?isHttpsRedirect=true&blogId=jsky10503&logNo=220743902613)

`/etc/group`과 `/etc/gshadow`를 관리한다.ㄴ

```shell
# gpasswd를 사용하기 위한 패키지
apk add --no-cache shadow
```

## 그룹에 유저 추가
```shell
gpasswd -a [USER] [GROUP]
```

## 그룹에서 유저 삭제
```shell
gpasswd -d [USER] [GROUP]
```

# apk trust host 인증서 문제 해결법
> 참고: [Alpine Linux - apk trust host 인증서 문제 해결
](https://asecurity.dev/entry/Alpine-Linux-apk-trust-host-%EC%9D%B8%EC%A6%9D%EC%84%9C-%EB%AC%B8%EC%A0%9C-%ED%95%B4%EA%B2%B0)

apk를 이용하여 add나 update를 할 때 `tls process server certificate:certificate verify` 에러가 발생한다면

```shell
sed 's/https/http/g' -i /etc/apk/repositories
```

도커 이미지에 위의 내용을 RUN 한 후, `apk add/update`를 RUN 한다.

# ssh 설정
ssh를 설정할 때 Born2beroot와는 다른 점이 몇 가지 있어서 그 점을 정리하려 한다.

기본적인 세팅은 [Born2beroot를 마치고 - ssh](/42_seoul/born2beroot/#ssh) 부분부터 포트 포워딩까지와 같다.

## /etc/ssh/sshd_config
vim으로 해당 파일을 설정할 때 `#Port 22` 부분을 주석 해제하고 포드 번호를 지정하는 건 같다.

그리고 `PermitRootLogin` 부분은 `setup-alpine` 명령어를 실행했을 때 루트 로그인 제한할거냐는 물음에 no라고 답했기 때문에 건드리지 않았다.

## ssh 재시작
```shell
/etc/init.d/sshd restart
```

데비안 때에는 `systemctl`로 재시작 했는데, 이 부분이 달랐다.

## + ip 설정 따로 안 했음
이번에는 고정 ip를 사용해서 하지 않았기 때문에 ssh로 UTM에서 네트워크 설정에서 ip를 따로 입력해주지 않았고 포트만 4242->4242로만 해줬다.

마찬가지로 터미널에서 ssh로 접속할 때에도 `user@127.0.0.1` 같이 ip를 직접 지정해주지 않고 `user@localhost`와 같은 방식을 사용했다.
