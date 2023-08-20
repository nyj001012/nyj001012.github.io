---
title: "[Inception] setup alpine"
excerpt: "알파인 리눅스 셋업"
category: 
  - 42_seoul
author_profile: true
sidebar:
  - nav: "main" 
tag:
  - 42서울
toc: true
toc_sticky: true
last_modified_at: 2023-08-20T00:00:00+09:00
---

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
