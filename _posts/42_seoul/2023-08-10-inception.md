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
last_modified_at: 2023-08-10T00:00:00+09:00
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

## apk trust host 인증서 문제 해결법
> 참고: [Alpine Linux - apk trust host 인증서 문제 해결
](https://asecurity.dev/entry/Alpine-Linux-apk-trust-host-%EC%9D%B8%EC%A6%9D%EC%84%9C-%EB%AC%B8%EC%A0%9C-%ED%95%B4%EA%B2%B0)

apk를 이용하여 add나 update를 할 때 `tls process server certificate:certificate verify` 에러가 발생한다면

```shell
sed 's/https/http/g' -i /etc/apk/repositories
```

도커 이미지에 위의 내용을 RUN 한 후, `apk add/update`를 RUN 한다.
