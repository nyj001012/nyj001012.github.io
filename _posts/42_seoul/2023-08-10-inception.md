---
title: "inception"
excerpt: "inception 과제 하면서 정리한 것들"
category: 
  - 42_seoul
author_profile: true
sidebar:
  - nav: "main" 
tag:
  - 42서울
toc: true
toc_sticky: true
last_modified_at: 2023-08-14T00:00:00+09:00
---

# 왜 Alpine Linux인가?
> 참고: [왜 컨테이너 환경에서는 Alpine Linux가 선호될까?](https://velog.io/@dry8r3ad/why-alpine-linux)

1. 용량이 작음
2. 보안

# Alpine Linux 설치 사이트
<https://www.alpinelinux.org/downloads/>

(m1 UTM virtual aarch64 사용)

# Alpine Linux 세팅
## 기본 설치
> 참고: [How to Install Alpine Linux on VirtualBox
](https://linuxhint.com/install-alpine-linux-virtualbox/)
> 
> 공식 문서: <https://docs.alpinelinux.org/user-handbook/0.1a/Installing/setup_alpine.html>

### 최초 로그인 시 user
```
root
```

### 설치 명령어
```shell
> setup-alpine
```

## 알파인 리눅스의 패키지 관리자
apk

## 타임존 설정 방법 (2가지)
사실 초기 세팅 단계에서 Korea가 안 보여서 지원을 안 하는 줄 알았다. 그래서 찾은 게 tzdata인데, 여기에서 서울 데이터를 따로 들고와서 세팅해야하나 싶었다. 그런데 알고보니 초기 세팅 단계에서 그냥 Asia -> Seoul을 선택하면 됐었다...

### TZ 환경 변수 설정
> 참고: [공식 문서 Timezone
](https://docs.alpinelinux.org/user-handbook/0.1a/Installing/manual.html#_timezone)

tzdata 설치
```shell
> apk --no-cache add tzdata
```

타임존 파일 복사
```shell
> install -Dm 0644 /usr/share/zoneinfo/Asia/Seoul /etc/zoneinfo/Asia/Seoul
```

TZ 환경변수 설정
```shell
> export TZ='Asia/Seoul' 
echo "export TZ='$TZ'" >> /etc/profile.d/timezone.sh
```

### localtime-style
```shell
setup-timezone
```

# 과제 진행
> 참고: [Inception (팔만코딩경)
](https://bigpel66.oopy.io/library/42/inner-circle/20)

## 세팅
### 패키지 설치
> 참고: [linux apk 사용법, 설명](https://amkorousagi-money.tistory.com/entry/linux-apk-%EC%82%AC%EC%9A%A9%EB%B2%95-%EC%84%A4%EB%AA%85)
> 
> 알파인 리눅스 패키지 허브 페이지: <https://pkgs.alpinelinux.org/packages>

설치를 할 때 나는 `--no-cache` 옵션을 많이 사용했는데, 이러면 로컬에 저장된 apk 인덱스 대신 새로 패키지 인덱스를 다운로드(fetch가 출력된다)하여 설치한다. 그러면 패키지의 최신 버전을 사용할 수 있다는 장점이 있지만, 네트워크 이용량이 많아진다는 단점이 있다.

사실 난 로컬 캐시가 없을 것이기 때문에 옵션을 사용하든 안 하든 상관은 없었다.

```shell
# 루트 사용자로 전환(su; switch user)
su

# 패키지 인덱스 업데이트
apk update

# CA 인증서 추가
apk add --no-cache ca-certificates

# curl 추가
apk add --no-cache curl

# git 추가
apk add --no-cache git

# make 추가
apk add --no-cache make

# vim 추가
apk add --no-cache vim
```

### Docker 설치
> 참고: [Alpine Linux Docker 설치하기
](https://svrforum.com/os/119006)

#### 커뮤니티 레포지토리 추가
```shell
vim /etc/apk/repositories
```

위의 명령어를 사용하면

![레포지토리](/assets/images/page/42_seoul/2023-08-12_repositories.png)

이런 파일이 열릴텐데, 세 번째 줄인 `community`가 적힌 줄을 주석 해제한다.

#### Docker
```shell
# 인덱스 업데이트
apk update

# 도커 설치
apk add --no-cache docker

# 부팅 시 docker 데몬 실행
rc-update add docker boot
service docker start
```

위의 두 명령어를 실행하면 아래와 같은 화면이 나온다.

![레포지토리](/assets/images/page/42_seoul/2023-08-12_docker_install_result.png)

```shell
# 도커 소켓에 다른 사용자도 접근 가능하게 변경
chmod 666 /var/run/docker.sock

# docker-compose 설치
apk add --no-cache docker-compose

# 재시작
reboot
```

설치 완료 후, 아래의 명령어를 입력하면 다음과 같은 결과가 출력된다. `openrc` 세팅까지 완료했기 때문에, Server 항목도 표시되어야 한다.

```shell
docker version
```

![docker_setting_complete](/assets/images/page/42_seoul/2023-08-12_docker_setting_complete.png)

## GUI
> 참고: [How to install XFCE GUI on Alpine Linux
](https://linux.how2shout.com/how-to-install-xfce-gui-on-alpine-linux/)

나는 그냥 CLI 환경에서 과제를 진행하려 했으나..? 과제에 대해 조언을 구한 멤버 분으로부터 브라우저를 이용해야 한다는 평가 항목이 있다는 얘기를 들었다. 그래서 급하게 GUI를 추가했다.

![alpin_gui](../../assets/images/page/42_seoul/2023-08-14_gui.png)

짠!

### 세팅 과정
```shell
# 윈도우 시스템 디스플레이 서버(Xorg) 설치
setup-xorg-base

# 경량 데스크탑 환경인 XFCE 설치
apk add xfce4 xfce4-terminal xfce4-screensaver lightdm-gtk-greeter

# dbus(;desktop bus) 서비스 시작
rc-service dbus start

# 부트 시, 자동으로 서비스 시작
rc-update add dbus

# 부트 시, 자동으로 display manager 시작
rc-update add lightdm

# display manager 수동 시작
rc-service lightdm start
```

# docker-compose
> 공식 문서: <https://docs.docker.com/compose/gettingstarted/>

## 파일 구성
> 공식 문서: <https://docs.docker.com/compose/compose-file/compose-file-v3/>

docker-compose의 파일 예시를 봤는데, 궁금한 점이 있어서 찾아보고 정리했다.

### version
.yml 파일 보면 맨 첫 줄에 항상

```yml
version: '3.8'
```

이런 식으로 적혀 있는 걸 봤는데, 이는 compose 파일의 버전이다. 도커 버전에 맞는 compose 파일의 버전을 명시해야 하며, version 1.x와 2.x, 3.x가 구성 파일의 매개 변수가 삭제되었거나 추가된 것들이 있다. 해당 내용은 [Docker Compose와 버전별 특징
](https://meetup.nhncloud.com/posts/277)을 참고하면 좋을 것 같다.

### services
compose 파일은 서비스 이름의 문자열 표현을 키로, 서비스 정의를 값으로 하는 맵으로 선언되어야 한다. 서비스 정의에는 각 서비스 컨테이너에 적용되는 구성이 포함된다.

각 서비스에는 반드시 서비스의 도커 이미지를 어떻게 생성할지를 정의한 `build` 섹션이 있어야 한다.

그 외에 services에 정의할 수 있는 섹션은 아래와 같다.
- build: [Compose Build Specification](https://docs.docker.com/compose/compose-file/build/)에 정의된 대로 소스를 컨테이너 이미지로 만들기 위한 빌드 설정을 정의한다.

이 내용들과 Docker hub에서 패키지들의 "... via docker-compose or docker stack deploy" 섹션을 토대로 작성한 내용은 다음과 같았다.

```yml
version: '3.8'

services:
  nginx:
    image: nginx
    volumes:
      - ./templates:/etc/nginx/templates
    ports:
      - 8080:80
    environment:
      - NGINX_HOST=foobar.com
      - NGINX_PORT=80
  
  mariadb:
    image: mariadb
    restart: always
    environment:
      MARIADB_ROOT_PASSWORD: example

  wordpress:
    image: wordpress
    restart: always
    ports:
      - 8000:80
    environment:
      WORDPRESS_DB_HOST: mariadb
      WORDPRESS_DB_USER: exampleuser
      WORDPRESS_DB_PASSWORD: examplepass
      WORDPRESS_DB_NAME: exampledb
```

그리고 `docker-compose up`을 해 보니 이미지 생성은 전부 잘 됐다.

### volumes

### .env

# 알파인 리눅스를 사용하며 배운 것
## sudo, usermod 없음
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

## 그룹 관리를 더 편하게 할 수 있도록 도와주는 gpasswd

> 참고: [리눅스-gpasswd 명령어](https://m.blog.naver.com/PostView.nhn?isHttpsRedirect=true&blogId=jsky10503&logNo=220743902613)

`/etc/group`과 `/etc/gshadow`를 관리한다.ㄴ

```shell
# gpasswd를 사용하기 위한 패키지
apk add --no-cache shadow
```

### 그룹에 유저 추가
```shell
gpasswd -a [USER] [GROUP]
```

### 그룹에서 유저 삭제
```shell
gpasswd -d [USER] [GROUP]
```

## apk trust host 인증서 문제 해결법
> 참고: [Alpine Linux - apk trust host 인증서 문제 해결
](https://asecurity.dev/entry/Alpine-Linux-apk-trust-host-%EC%9D%B8%EC%A6%9D%EC%84%9C-%EB%AC%B8%EC%A0%9C-%ED%95%B4%EA%B2%B0)

apk를 이용하여 add나 update를 할 때 `tls process server certificate:certificate verify` 에러가 발생한다면

```shell
sed 's/https/http/g' -i /etc/apk/repositories
```

도커 이미지에 위의 내용을 RUN 한 후, `apk add/update`를 RUN 한다.

## ssh 설정
ssh를 설정할 때 Born2beroot와는 다른 점이 몇 가지 있어서 그 점을 정리하려 한다.

기본적인 세팅은 [Born2beroot를 마치고 - ssh](./2022-12-12-born2beroot.md/#ssh) 부분부터 포트 포워딩까지와 같다.

### /etc/ssh/sshd_config
vim으로 해당 파일을 설정할 때 `#Port 22` 부분을 주석 해제하고 포드 번호를 지정하는 건 같다.

그리고 `PermitRootLogin` 부분은 `setup-alpine` 명령어를 실행했을 때 루트 로그인 제한할거냐는 물음에 no라고 답했기 때문에 건드리지 않았다.

### ssh 재시작
```shell
/etc/init.d/sshd restart
```

데비안 때에는 `systemctl`로 재시작 했는데, 이 부분이 달랐다.

### + ip 설정 따로 안 했음
이번에는 고정 ip를 사용해서 하지 않았기 때문에 ssh로 UTM에서 네트워크 설정에서 ip를 따로 입력해주지 않았고 포트만 4242->4242로만 해줬다.

마찬가지로 터미널에서 ssh로 접속할 때에도 `user@127.0.0.1` 같이 ip를 직접 지정해주지 않고 `user@localhost`와 같은 방식을 사용했다.
