---
title: "[Inception] install package"
excerpt: "패키지 설치"
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

> 참고: [Inception (팔만코딩경)
](https://bigpel66.oopy.io/library/42/inner-circle/20)

# 세팅
## 패키지 설치
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

# Makefile 을 위한 make 추가
apk add --no-cache make
```

## Docker 설치
> 참고: [Alpine Linux Docker 설치하기
](https://svrforum.com/os/119006)

### 커뮤니티 레포지토리 추가
```shell
vim /etc/apk/repositories
```

위의 명령어를 사용하면

![레포지토리](/assets/images/page/42_seoul/2023-08-12_repositories.png)

이런 파일이 열릴텐데, 세 번째 줄인 `community`가 적힌 줄을 주석 해제한다.

### Docker
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
